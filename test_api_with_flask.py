import requests
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

DJANGO_API_URL = 'http://localhost:8000'

API_PATHS = {
    'users': '/users/',
    'users_register': '/users/register/',
    'token_login': '/users/token/login/',
    'posts': '/post/',
    'comments': '/comment/',
}


def test_api():
    print("🚀 Запуск тестов API через Flask...")
    print(f"🔗 Базовый URL: {DJANGO_API_URL}")

    test_endpoints()

    return jsonify({"message": "Тестирование завершено! Проверьте консоль."})


def test_endpoints():
    print("\n👥 ТЕСТИРОВАНИЕ ПОЛЬЗОВАТЕЛЕЙ")
    test_users()

    print("\n📝 ТЕСТИРОВАНИЕ ПОСТОВ")
    test_posts()

    print("\n💬 ТЕСТИРОВАНИЕ КОММЕНТАРИЕВ")
    test_comments()


def test_users():
    try:
        # 1. Сначала регистрируем пользователя
        user_data = {
            "login": f"flask_test_user_{requests.utils.quote('test')}",
            "email": "flask_test@mail.ru",
            "password": "Password123",  # Пароль с цифрой и заглавной буквой
            "password_confirm": "Password123"
        }

        print(f"🔧 Регистрация пользователя: {user_data['login']}")
        response = requests.post(
            DJANGO_API_URL + API_PATHS['users_register'],
            json=user_data,
            timeout=5
        )

        print(f"POST {API_PATHS['users_register']} - Status: {response.status_code}")

        if response.status_code == 201:
            print("✅ Пользователь успешно создан!")
            # Тестируем получение токена
            test_auth(user_data['login'], user_data['password'])
        else:
            print(f"❌ Ошибка регистрации: {response.text}")

    except Exception as e:
        print(f"❌ Ошибка при тестировании пользователей: {e}")


def test_auth(login, password):
    """Тестирование аутентификации"""
    try:
        auth_data = {
            "login": login,
            "password": password
        }
        response = requests.post(
            DJANGO_API_URL + API_PATHS['token_login'],
            json=auth_data,
            timeout=5
        )

        print(f"POST {API_PATHS['token_login']} - Status: {response.status_code}")

        if response.status_code == 200:
            token = response.json().get('token')
            print(f"✅ Токен получен: {token[:20]}...")
            return token
        else:
            print(f"❌ Ошибка аутентификации: {response.text}")

    except Exception as e:
        print(f"❌ Ошибка аутентификации: {e}")
    return None


def test_posts():
    try:
        response = requests.get(
            DJANGO_API_URL + API_PATHS['posts'],
            timeout=5
        )
        print(f"GET {API_PATHS['posts']} - Status: {response.status_code}")

        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Найдено постов: {len(posts)}")
        else:
            print(f"❌ Ошибка: {response.text}")

    except Exception as e:
        print(f"❌ Ошибка при тестировании постов: {e}")


def test_comments():
    try:
        response = requests.get(
            DJANGO_API_URL + API_PATHS['comments'],
            timeout=5
        )
        print(f"GET {API_PATHS['comments']} - Status: {response.status_code}")

        if response.status_code == 200:
            comments = response.json()
            print(f"✅ Найдено комментариев: {len(comments)}")
        else:
            print(f"❌ Ошибка: {response.text}")

    except Exception as e:
        print(f"❌ Ошибка при тестировании комментариев: {e}")


@app.route('/')
def home():
    return test_api()


@app.route('/test/simple')
def test_simple():
    """Простое тестирование только работающих эндпоинтов"""
    print("🧪 Простое тестирование...")

    # Тестируем только комментарии (они работают)
    test_comments()

    # Пробуем посты с обработкой ошибок
    try:
        response = requests.get(DJANGO_API_URL + API_PATHS['posts'])
        if response.status_code == 500:
            print("⚠️  Посты возвращают 500 - нужно смотреть логи Django")
        else:
            print(f"📝 Посты: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка постов: {e}")

    return jsonify({"message": "Простое тестирование завершено"})


if __name__ == '__main__':
    print("🌐 Запуск Flask-сервера для тестирования API...")
    app.run(debug=True, port=5000)
