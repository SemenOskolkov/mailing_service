import os
from django import template
from mailing.models import MailingSettings

register = template.Library()


@register.simple_tag
def mailing_count():
    count = MailingSettings.objects.all().count()
    return count


@register.simple_tag
def mail_count_activ():
    count = MailingSettings.objects.filter(mailing_status=MailingSettings.STATUS_LAUNCHED).count()
    return count