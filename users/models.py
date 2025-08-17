from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.DRY import NULLABLE


class CustomUser(AbstractUser):
    """
    Модель пользователя
    """
    username = None

    login = models.Field(
        max_length=50,
        unique=True,
        verbose_name='Логин',
        help_text=_('Уникальный логин пользователя')
    )

    password = models.CharField(
        _('password'),
        max_length=128,
    )

    phone_number = models.CharField(
        max_length=15,
        **NULLABLE,
        verbose_name='Номер телефона',
        help_text=_('Номер в международном формате')
    )

    birthdate = models.DateField(
        **NULLABLE,
        verbose_name='Дата рождения',
        help_text=_('Формат: YYYY-MM-DD')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login or self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
