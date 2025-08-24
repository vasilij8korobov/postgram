import re
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_password_complexity(value):
    """Валидатор пароля: минимум 8 символов и цифры"""
    if len(value) < 8:
        raise ValidationError(
            _('Пароль должен содержать минимум 8 символов.'),
            code='password_too_short'
        )

    if not any(char.isdigit() for char in value):
        raise ValidationError(
            _('Пароль должен содержать хотя бы одну цифру.'),
            code='password_no_digit'
        )


def validate_email_domain(value):
    """Валидатор email: разрешены только mail.ru и yandex.ru"""
    allowed_domains = ['mail.ru', 'yandex.ru']
    domain = value.split('@')[-1] if '@' in value else ''

    if domain not in allowed_domains:
        raise ValidationError(
            _('Разрешены только почтовые адреса с доменами: %(domains)s'),
            code='invalid_domain',
            params={'domains': ', '.join(allowed_domains)}
        )


def validate_adult_age(birthdate):
    """Валидатор возраста: проверка что пользователю есть 18 лет"""
    if birthdate:
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if age < 18:
            raise ValidationError(
                _('Автор должен быть старше 18 лет.'),
                code='underage_author'
            )


def validate_title_no_bad_words(value):
    """Валидатор заголовка: проверка на запрещенные слова"""
    forbidden_words = ['ерунда', 'глупость', 'чепуха']
    words = value.lower().split()

    for bad_word in forbidden_words:
        if bad_word in words:
            raise ValidationError(
                _('Заголовок содержит запрещенное слово: "%(word)s"'),
                code='forbidden_word',
                params={'word': bad_word}
            )