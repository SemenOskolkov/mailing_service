from django.contrib.auth.models import AbstractUser
from django.db import models

from base.models import NULLABLE


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=25, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='UsersAvatar/', **NULLABLE, verbose_name='Аватар')
    country = models.CharField(max_length=100, verbose_name='Страна')
    token = models.CharField(max_length=15, verbose_name='токен', blank=True, null=True)
    new_password = models.CharField(verbose_name="новый пароль", max_length=128, **NULLABLE)

