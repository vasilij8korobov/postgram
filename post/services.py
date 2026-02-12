from django.core.exceptions import ValidationError
from config.validators import validate_adult_age


class PostService:
    """Сервис для бизнес-логики постов"""

    @staticmethod
    def validate_post_author_age(author):
        """Валидация возраста автора поста"""
        if author and author.birthdate:
            validate_adult_age(author.birthdate)

    @staticmethod
    def create_post(validated_data, author):
        """Создание поста с валидацией бизнес-правил"""
        from .models import Post

        # Создаем объект поста
        post = Post(**validated_data)
        post.author = author

        # Валидируем бизнес-правила
        PostService.validate_post_author_age(post)

        # Сохраняем
        post.save()
        return post