from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.DRY import NULLABLE
from config.validators import validate_email_domain


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели пользователя с login вместо username"""

    def create_user(self, login, email, password=None, **extra_fields):
        """Создает и возвращает пользователя с login, email и паролем"""
        if not email:
            raise ValueError('У пользователя должна быть почта')
        if not login:
            raise ValueError('У пользователя должен быть логин')

        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(login, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Модель пользователя
    """
    username = None

    login = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Логин',
        help_text=_('Уникальный логин пользователя')
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[validate_email_domain],
        help_text=_('Разрешены только mail.ru и yandex.ru')
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

    def clean(self):
        """Валидация на уровне модели"""
        super().clean()
        if self.birthdate:
            from config.validators import validate_adult_age
            validate_adult_age(self.birthdate)

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию при сохранении
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.login or self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
