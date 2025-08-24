from config.validators import *


# Тест пароля
try:
    validate_password_complexity('short')
    print("ERROR: Короткий пароль прошел валидацию")
except ValidationError as e:
    print("OK: Короткий пароль отловлен")


# Тест email
try:
    validate_email_domain('test@gmail.com')
    print("ERROR: Запрещенный домен прошел валидацию")
except ValidationError as e:
    print("OK: Запрещенный домен отловлен")


# Тест заголовка
try:
    validate_title_no_bad_words('Это ерунда какая-то')
    print("ERROR: Запрещенное слово прошел валидацию")
except ValidationError as e:
    print("OK: Запрещенное слово отловлено")
