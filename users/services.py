from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from users.models import User


def send_verify_token_on_email(new_user):
    now = datetime.now(pytz.timezone(settings.TIME_ZONE))
    new_user.is_active = False
    new_user.token = User.objects.make_random_password(length=35)
    new_user.token_time = now + timedelta(hours=24)
    new_user.save()
    send_mail(
        subject='Подтверждение почты для сайта "Owl mailing"',
        message=f' http://127.0.0.1:8000/users/activate/{new_user.token}/',
        recipient_list=[new_user.email],
        from_email=settings.EMAIL_HOST_USER,
    )


def generate_password_and_send_mail(user):
    new_password = User.objects.make_random_password(length=12)
    user.new_password = make_password(new_password)
    user.save()
    send_mail(
        subject='Новый пароль',
        message=f'{new_password}',
        recipient_list=[user.email],
        from_email=settings.EMAIL_HOST_USER
    )