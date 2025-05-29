from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
