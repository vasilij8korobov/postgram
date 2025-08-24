import os
import django
from datetime import date
from django.core.exceptions import ValidationError

# Настраиваем Django окружение ДО импортов моделей
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from post.services import PostService
from users.models import CustomUser


def test_post_validators():
    """Тестирование валидаторов постов"""

    print("🧪 Тестирование валидации возраста автора...")

    # Создаем тестовых пользователей
    adult_user = CustomUser.objects.create_user(
        login='adult_test',
        email='adult_test@mail.ru',
        password='password123',
        birthdate=date(2000, 1, 1)  # Взрослый
    )

    # teen_user = CustomUser.objects.create_user(
    #     login='teen_test',
    #     email='teen_test@mail.ru',
    #     password='password123',
    #     birthdate=date(2010, 1, 1)  # Несовершеннолетний
    # )

    # Тест 1: Взрослый автор должен проходить валидацию
    try:
        PostService.validate_post_author_age(adult_user)
        print("✅ Взрослый автор прошел валидацию")
    except ValidationError as e:
        print(f"❌ Ошибка: {e}")

    # Тест 2: Несовершеннолетний автор должен вызывать ошибку
    # try:
    #     PostService.validate_post_author_age(teen_user)
    #     print("❌ Несовершеннолетний автор прошел валидацию (это ошибка!)")
    # except ValidationError as e:
    #     print(f"✅ Несовершеннолетний автор отловлен: {e}")

    # Тест 3: Пользователь без даты рождения
    user_no_birthdate = CustomUser.objects.create_user(
        login='no_birth_test',
        email='no_birth@mail.ru',
        password='password123'
        # Нет birthdate
    )

    try:
        PostService.validate_post_author_age(user_no_birthdate)
        print("✅ Пользователь без даты рождения прошел валидацию")
    except ValidationError as e:
        print(f"❌ Ошибка для пользователя без даты рождения: {e}")


if __name__ == "__main__":
    test_post_validators()