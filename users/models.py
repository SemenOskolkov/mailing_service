from django.contrib.auth.models import AbstractUser
from django.db import models

from base.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=25, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='UsersAvatar/', **NULLABLE, verbose_name='Аватар')
    country = models.CharField(max_length=100, verbose_name='Страна')
    token = models.CharField(max_length=15, blank=True, null=True, verbose_name='Токен')
    new_password = models.CharField(max_length=128, **NULLABLE, verbose_name="Новый пароль")
    token_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания токена')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('can_block_users_of_service', 'Can block users of the service'),
        ]