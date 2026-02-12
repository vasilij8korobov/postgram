from django.db import models
from django.utils.translation import gettext_lazy as _
from config.DRY import NULLABLE
from django.conf import settings

from config.validators import validate_password_complexity, validate_title_no_bad_words


class Post(models.Model):
    """
    Модель поста
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Автор')
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок',
        help_text=_('Максимум 255 символов'),
        validators=[validate_title_no_bad_words]
    )

    text = models.TextField(verbose_name='Начните писать текст')

    image = models.ImageField(
        upload_to='images/posts/',
        **NULLABLE,
        verbose_name='Изображение'
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateField(
        auto_now=True,
        verbose_name='Дата редактирования'
    )

    def clean(self):
        """Валидация возраста автора"""
        super().clean()
        if self.author and self.author.birthdate:
            from config.validators import validate_adult_age
            validate_adult_age(self.author.birthdate)

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию при сохранении
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author} | {self.title}"

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
