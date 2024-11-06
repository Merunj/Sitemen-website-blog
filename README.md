# Sitemen

**Sitemen** — это сайт для публикации статей о мужчинах из различных сфер жизни, также можно добавить своего кумира. Любой пользователь может зарегистрироваться, добавлять и редактировать собственные статьи, а также просматривать статьи по категориям и тегам.

## Функциональные возможности

- **Добавление статей**: зарегистрированные пользователи могут публиковать свои статьи.
- **Редактирование статей**: возможность редактировать только свои собственные статьи.
- **Регистрация**: стандартная регистрация и авторизация через OAuth 2.0 (GitHub).
- **Восстановление пароля**: функция восстановления пароля для зарегистрированных пользователей.
- **Навигация**: фильтрация статей по категориям и тегам.

## Стек

- **Backend**: Django
- **База данных**: PostgreSQL
- **Кэширование**: Redis
- **Аутентификация**: OAuth 2.0 (включая возможность входа через GitHub)

## Установка и запуск проекта

### Предварительные требования

Перед запуском убедитесь, что у вас установлены:

- Python 3.x
- Django 5.x
- Redis
- PostgreSQL

### Установка

1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/Merunj/sitemen.git
   cd sitemen
   ```
2. **Установите зависимости**:
   Рекомендуется использование виртуального окружения:
   ```bash
   python -m venv venv
   source venv/bin/activate   # для Linux / macOS
   venv\Scripts\activate      # для Windows
   ```
   Затем установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```
3. **Настройка SMPT-сервера Яндекс**:
   ```python
   EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

   EMAIL_HOST = 'smtp.yandex.ru'
   EMAIL_PORT = 465
   EMAIL_HOST_USER = "YOUR YANDEX E-MAIL"
   EMAIL_HOST_PASSWORD = "YOUR APP PASSWORD"
   EMAIL_USE_SSL = True
    
   DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
   SERVER_EMAIL = EMAIL_HOST_USER
   EMAIL_ADMIN = EMAIL_HOST_USER
   ```
4. **Запуск сервера**:
   После того, как вы убедились, что работает redis-server, запустите сервер Django командой:
   ```python
   python manage.py runserver
   ```
   
   
   
   
