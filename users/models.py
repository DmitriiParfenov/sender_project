from django.contrib.auth.models import AbstractUser
from django.db import models

from clients.models import NULLABLE


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=30, verbose_name='номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=150, verbose_name='страна', **NULLABLE)
    user_identity = models.CharField(max_length=20, verbose_name='ключ', **NULLABLE)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'set_disabled',
                'Can disable Пользователь'
            )
        ]

