# Yandex Afisha
Фронтенд для будущего сайта о самых интересных местах в Москве.

<img width="1907" height="907" alt="image" src="https://github.com/user-attachments/assets/ecc257d2-a49b-4b3d-894c-d529655d9043" />

Проект представляет собой сайт с картой мест. Каждая локация имеет:
- Короткое описание (для показа на карте),
- Длинное описание с HTML-разметкой,
- Одно или несколько изображений,
- Координаты (широта и долгота).

Админка позволяет управлять локациями и загружать изображения через удобный интерфейс с WYSIWYG-редактором (CKEditor).

## Требования

- Python 3.11+
- Django 4.x+
- PostgreSQL / SQLite

## Переменные окружения

Все чувствительные настройки вынесены в `.env`. Пример:

| Переменная           | Описание                                   | Пример                     |
|----------------------|--------------------------------------------|----------------------------|
| DJANGO_SECRET_KEY     | Секретный ключ Django                       | dev-secret-key             |
| DJANGO_DEBUG          | Режим дебага (True/False)                  | True                       |
| DJANGO_ALLOWED_HOSTS  | Список разрешённых хостов через запятую   | 127.0.0.1,localhost       |
| DJANGO_DB_ENGINE      | Драйвер базы данных                         | django.db.backends.sqlite3 |
| DJANGO_DB_NAME        | Имя базы данных                             | db.sqlite3                 |
| DJANGO_DB_USER        | Пользователь БД (для Postgres/MySQL)       | myuser                     |
| DJANGO_DB_PASSWORD    | Пароль БД                                  | mypassword                 |
| DJANGO_DB_HOST        | Хост БД                                    | 127.0.0.1                  |
| DJANGO_DB_PORT        | Порт БД                                    | 5432                       |

> Для локальной разработки можно использовать SQLite и `DEBUG=True`.

## Установка и запуск локально

1. Клонируем репозиторий:

```
cd yandex_afisha
```
Создаём виртуальное окружение и активируем:
```
python -m venv venv
```
# Windows
```
venv\Scripts\activate
```
# Linux / Mac
```
source venv/bin/activate
```
Устанавливаем зависимости:

bash
Копировать код
pip install -r requirements.txt
Создаём файл .env (см. пример выше).

Применяем миграции:
```
python manage.py migrate
```
Создаём суперпользователя:
```
python manage.py createsuperuser
```
Запускаем сервер:
```
python manage.py runserver
```
Админка
Доступ: [Админка Django](http://127.0.0.1:8000/admin/)

Модели:

Place — локации с описаниями и координатами.

PlaceImage — изображения локаций.

Массовая загрузка данных
Поместите JSON-файлы с локациями в static/places/.

Используйте команду:
```
python manage.py load_place
```
Локации с уже существующим title пропускаются.

JSON-файл должен быть массивом объектов:
```
[
  {
    "title": "Красная площадь",
    "short_description": "Центральная площадь Москвы",
    "long_description": "Здесь проходят основные праздники и парады",
    "latitude": 55.7539,
    "longitude": 37.6208
  }
]
```

.env — переменные окружения

venv/ — виртуальное окружение

staticfiles/ — собранные статики

uploads/ — CKEditor
