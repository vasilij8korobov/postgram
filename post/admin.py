from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from rest_framework.exceptions import ValidationError

from .models import Post
from django.utils.translation import gettext_lazy as _

from .services import PostService


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get('author')

        post = Post(**cleaned_data)

        if author:
            try:
                PostService.validate_post_author_age(author)  # ← Передаем автора, а не пост
            except ValidationError as e:
                self.add_error('author', e)

        return cleaned_data


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админ-панель для постов"""

    form = PostAdminForm
    list_display = ['title', 'author_link', 'created_at', 'updated_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'text', 'author__login']
    readonly_fields = ['created_at', 'updated_at', 'author_link']
    date_hierarchy = 'created_at'

    def author_link(self, obj):
        """Ссылка на автора в админке"""
        if obj.author:
            url = reverse('admin:users_customuser_change', args=[obj.author.id])
            return format_html('<a href="{}">{}</a>', url, obj.author.login)
        return _("Нет автора")

    author_link.short_description = _("Автор (ссылка)")

    def get_queryset(self, request):
        """Оптимизация запроса - предзагрузка автора"""
        return super().get_queryset(request).select_related('author')
