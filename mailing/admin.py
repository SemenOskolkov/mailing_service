from django.contrib import admin

from mailing.models import Client, MailingSettings, Message, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'comment',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'period', 'mailing_status', 'message',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('letter_subject', 'letter_body',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('last_datetime', 'status', 'server_response', 'settings',)