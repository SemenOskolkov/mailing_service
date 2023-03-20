from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User
from users.services import send_verify_token_on_email, generate_password_and_send_mail


class UserLoginView(LoginView):  # Авторизация
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegisterView(CreateView):  # Регистрация
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:register_success')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            send_verify_token_on_email(self.object)
            self.object.is_active = True
            self.object.save()
        return super().form_valid(form)


class RegisterSuccessView(TemplateView):
    template_name = 'users/register_success.html'


class VerifySuccessView(TemplateView):
    template_name = 'users/verify_success.html'


def verify_email(request, token):
    current_user = User.objects.filter(verify_token=token).first()
    if current_user:
        now = datetime.now(pytz.timezone(settings.TIME_ZONE))
        if now > current_user.token_time:
            current_user.delete()
            return render(request, 'users/verify_token_expired.html')

        current_user.is_active = True
        current_user.token = None
        current_user.token_time = None
        current_user.save()
        return redirect('users:login')

    return render(request, 'users/verify_failed.html')


class UserProfileView(UpdateView):  # Изменение профиля
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    success_url = '/'
    template_name = 'users/change_password.html'


def simple_reset_password(request):  # Смена пароля. Пароль приходит на почту
    if request.method == 'POST':
        current_user = User.objects.filter(email=request.POST.get('email')).first()
        if current_user:
            generate_password_and_send_mail(current_user)
    return render(request, 'users/simple_reset.html')


def confirm_new_generated_password(request):
    current_user = User.objects.filter(email=request.GET.get('email')).first()
    current_user.password = current_user.new_password
    current_user.new_password = None
    current_user.save()


def user_activation(request, token):
    u = User.objects.filter(token=token)

    return redirect(reverse('mailing:home'))


class UsersListView(UserPassesTestMixin, ListView):
    """Просмотр списка зарегистрированных пользователей"""
    model = User
    template_name = 'users/users_list.html'

    def test_func(self):
        return self.request.user.has_perm("users.view_user")


@permission_required(perm='user.can_block_users_of_service')
def change_user_status(request, pk):
    """Смена статуса пользователя"""
    obj = get_object_or_404(User, pk=pk)
    if obj.is_active:
        obj.is_active = False
    else:
        obj.is_active = True
    obj.save()

    return redirect(request.META.get('HTTP_REFERER'))