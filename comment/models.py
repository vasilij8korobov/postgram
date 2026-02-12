from django.db import models
from django.utils.translation import gettext_lazy as _

from django.conf import settings


class Comment(models.Model):
    """
    Модель комментария
    """
    post = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE,
        verbose_name=_("Пост"),
        related_name='post_comments',
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Автор")
    )

    text = models.TextField(verbose_name=_("Текст"))

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    updated_at = models.DateField(
        auto_now=True,
        verbose_name=_('Дата редактирования')
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['created_at']
