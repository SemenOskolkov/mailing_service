from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from blog.models import Blog
from mailing.forms import ClientForm, MailingSettingsForm, MessageForm
from mailing.models import Client, MailingSettings, Message, MailingAttempt
from django.urls import reverse_lazy, reverse


class HomePageView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog'] = Blog.objects.filter(sign_publication=Blog.STATUS_ACTIVE).order_by('?')[:3]
        context_data['mailing_count'] = MailingSettings.objects.all().count()
        context_data['mailing_activ_count'] = MailingSettings.objects.filter(mailing_status=MailingSettings.STATUS_LAUNCHED).count()
        context_data['mailing_client_count'] = Client.objects.distinct('email').count()
        return context_data


'''CRUD model Client'''


class ClientListView(UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mailing/client/client_list.html'

    def test_func(self):
        return self.request.user.is_authenticated


class ClientCreateView(UserPassesTestMixin, CreateView):
    model = Client
    template_name = 'mailing/client/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        return self.request.user.is_authenticated


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    model = Client
    template_name = 'mailing/client/client_form.html'
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        client = self.get_object()
        if client.user == self.request.user:
            return True
        return self.request.user.is_superuser or self.request.user.has_perm('mailing.change_client')


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mailing/client/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        client = self.get_object()
        if client.user == self.request.user:
            return True
        return self.request.user.is_superuser or self.request.user.has_perm('mailing.delete_client')


'''CRUD model MailingSettings'''


class MailingSettingsListView(UserPassesTestMixin, ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_list.html'

    def test_func(self):
        return self.request.user.is_authenticated


class MailingSettingsCreateView(UserPassesTestMixin, CreateView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_form.html'
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_settings_list')

    def test_func(self):
        return self.request.user.is_authenticated


class MailingSettingsUpdateView(UserPassesTestMixin, UpdateView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_settings_list')

    def test_func(self):
        mailing_settings = self.get_object()
        if mailing_settings.user == self.request.user:
            return True
        return self.request.user.is_superuser or self.request.user.has_perm('mailing.change_mailing_settings')


class MailingSettingsDetailView(UserPassesTestMixin, DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_detail.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')

    def test_func(self):
        mailing_settings = self.get_object()
        if self.request.user == mailing_settings.user:
            return True
        return self.request.user.has_perm('mailing.view_mailing_settings')


class MailingSettingsDeleteView(UserPassesTestMixin, DeleteView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')

    def test_func(self):
        mailing_settings = self.get_object()
        if mailing_settings.user == self.request.user:
            return True
        return self.request.user.is_superuser or self.request.user.has_perm('mailing.delete_mailing_settings')


'''CRUD model Message'''


class MessageListView(UserPassesTestMixin, ListView):
    model = Message
    template_name = 'mailing/message/message_list.html'

    def test_func(self):
        return self.request.user.is_authenticated


class MessageCreateView(UserPassesTestMixin, CreateView):
    model = MailingSettings
    template_name = 'mailing/message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        return self.request.user.is_authenticated


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        message = self.get_object()
        if message.user == self.request.user:
            return True
        return self.request.user.is_superuser or self.request.user.has_perm('mailing.change_message')


class MessageDetailView(UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'mailing/message/message_detail.html'
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        message = self.get_object()
        if self.request.user == message.user:
            return True
        return self.request.user.has_perm('mailing.view_message')


class MessageDeleteView(UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'mailing/message/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        message = self.get_object()
        if message.user == self.request.user:
            return True
        return self.request.user.is_superuser or self.request.user.has_perm('mailing.delete_message')


'''CRUD model MailingAttempt'''


class MailingAttemptListView(UserPassesTestMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt/mailing_attempt_list.html'

    def test_func(self):
        return self.request.user.is_authenticated


class MailingAttemptDetailView(UserPassesTestMixin, DetailView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt/mailing_attempt_detail.html'
    success_url = reverse_lazy('mailing:mailing_attempt_list')

    def test_func(self):
        mailing_attempt = self.get_object()
        if self.request.user == mailing_attempt.user:
            return True
        return self.request.user.has_perm('mailing.view_mailing_attempt')


class MailingAttemptDeleteView(UserPassesTestMixin, DeleteView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt/mailing_attempt_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_attempt_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('mailing.delete_mailing_attempt')


@permission_required(perm='can_disable_mailings')
def change_status_settings(request, pk):
    '''Смена статуса настроек сообщения'''
    obj = get_object_or_404(MailingSettings, pk=pk)
    if obj.status == MailingSettings.STATUS_COMPLETED or obj.status == MailingSettings.STATUS_CREATED:
        obj.status = MailingSettings.STATUS_LAUNCHED
    elif obj.status == MailingSettings.STATUS_LAUNCHED:
        obj.status = MailingSettings.STATUS_COMPLETED
    obj.save()
    return redirect(request.META.get('HTTP_REFERER'))