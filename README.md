# VK Segmentation Service

## Описание

VK Segmentation Service — это сервис для хранения данных пользователей и их распределения по сегментам. Сервис позволяет создавать, изменять и удалять сегменты, добавлять и удалять пользователей в сегменты, а также случайным образом распределять сегменты на определённый процент пользователей. Предусмотрен API для получения списка сегментов по user_id.

Проект реализован на Django 4.2 и Django REST Framework с разделением на слои (models, services, serializers, views).

---

## Основные возможности
- CRUD для сегментов (создание, изменение, удаление)
- Добавление и удаление пользователей в сегменты
- Случайное распределение сегмента на процент пользователей
- Получение списка сегментов по user_id через API

---

## Запуск проекта

### Через Docker (рекомендуется)

1. Соберите и запустите контейнер:
   ```sh
   docker-compose up --build
   ```

2. Примените миграции (один раз после первого запуска):
   ```sh
   docker-compose run web python manage.py migrate
   ```

3. Откройте браузер и перейдите по адресу:
   [http://localhost:8000/api/](http://localhost:8000/api/)

---

### Альтернативно: Локальный запуск (без Docker)

1. Создайте и активируйте виртуальное окружение (Python 3.11.5):
   ```sh
   python3.11 -m venv venv
   source venv/bin/activate        # Linux/Mac
   # или
   venv\Scripts\activate          # Windows (cmd)
   # или
   source venv/Scripts/activate    # Windows (Git Bash)
   ```

2. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```

3. Примените миграции:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Запустите сервер:
   ```sh
   python manage.py runserver
   ```

5. Откройте браузер и перейдите по адресу:
   [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

## Примеры работы с API

- Создание сегмента: POST `/api/segments/`
- Добавление пользователя: POST `/api/users/create_user/` (указать id)
- Добавление пользователя в сегмент: POST `/api/segments/<segment_id>/add_user/` (указать user_id)
- Случайное распределение сегмента: POST `/api/segments/<segment_id>/assign_random_percent/` (указать percent)
- Получение сегментов пользователя: GET `/api/users/<user_id>/segments/`

---

## Автор
Raipus
