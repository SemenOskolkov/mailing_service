from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from mailing.forms import ClientForm, MailingSettingsForm, MessageForm
from mailing.models import Client, MailingSettings, Message, MailingAttempt
from django.urls import reverse_lazy, reverse


def home(request):
    return render(request, 'mailing/home.html')


'''CRUD model Client'''


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client/client_list.html'


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailing/client/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/client/client_form.html'
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')


'''CRUD model MailingSettings'''


class MailingSettingsListView(ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_list.html'


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_form.html'
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_settings_list')


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_settings_list')


class MailingSettingsDetailView(DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_detail.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings/mailing_settings_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')


'''CRUD model Message'''


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message/message_list.html'


class MessageCreateView(CreateView):
    model = MailingSettings
    template_name = 'mailing/message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailing/message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message/message_detail.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')


'''CRUD model MailingAttempt'''


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt/mailing_attempt_list.html'


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt/mailing_attempt_detail.html'
    success_url = reverse_lazy('mailing:mailing_attempt_list')


class MailingAttemptDeleteView(DeleteView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt/mailing_attempt_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_attempt_list')


def change_status_settings(request, pk):
    '''Смена статуса настроек сообщения'''
    obj = get_object_or_404(MailingSettings, pk=pk)
    if obj.status == MailingSettings.STATUS_COMPLETED or obj.status == MailingSettings.STATUS_CREATED:
        obj.status = MailingSettings.STATUS_LAUNCHED
    elif obj.status == MailingSettings.STATUS_LAUNCHED:
        obj.status = MailingSettings.STATUS_COMPLETED
    obj.save()
    return redirect(request.META.get('HTTP_REFERER'))