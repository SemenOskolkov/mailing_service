import os
from django import template
from mailing.models import Client

register = template.Library()


@register.simple_tag
def client_count():
    count = Client.objects.distinct('email').count()
    return count