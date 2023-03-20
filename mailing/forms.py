from django import forms

from base.forms import StyleFormMixin
from mailing.models import Client, MailingSettings, Message


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['owner', ]


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = '__all__'
        exclude = ['owner', ]


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'
        exclude = ['owner', ]