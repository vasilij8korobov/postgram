from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Comment
from django.utils.translation import gettext_lazy as _


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админ-панель для комментариев"""

    list_display = ['short_text', 'post_link', 'author_link', 'created_at']
    list_filter = ['created_at', 'post', 'author']
    search_fields = ['text', 'post__title', 'author__login']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    def short_text(self, obj):
        """Сокращенный текст комментария"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    short_text.short_description = _("Текст")

    def post_link(self, obj):
        """Ссылка на пост"""
        url = reverse('admin:post_post_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)

    post_link.short_description = _("Пост")

    def author_link(self, obj):
        """Ссылка на автора"""
        if obj.author:
            url = reverse('admin:users_customuser_change', args=[obj.author.id])
            return format_html('<a href="{}">{}</a>', url, obj.author.login)
        return _("Нет автора")

    author_link.short_description = _("Автор")

    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).select_related('post', 'author')