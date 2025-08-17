from django.db import models
from django.utils.translation import gettext_lazy as _
from config.DRY import NULLABLE
from django.conf import settings


class Post(models.Model):
    """
    Модель поста
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок',
        help_text=_('Максимум 255 символов')
    )

    text = models.TextField(verbose_name='Начните писать текст')

    image = models.ImageField(
        upload_to='images/posts/%Y/%m/%d/',
        **NULLABLE,
        verbose_name='Изображение'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Автор')
    )

    comment = models.ManyToManyField(  # Лучше отдельная модель для комментариев
        'Comment',
        related_name='post_comments',
        verbose_name='Комментарий',
        **NULLABLE
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateField(
        auto_now=True,
        verbose_name='Дата редактирования'
    )

    def __str__(self):
        return f"{self.author} | {self.title}"

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
