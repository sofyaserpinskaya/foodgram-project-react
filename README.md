# FOODGRAM - Продуктовый помощник

![foodgram_workflow](https://github.com/sofyaserpinskaya/foodgram-project-react/workflows/foodgram_workflow/badge.svg)

## Описание

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других авторов, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Автор

Backend - Софья Серпинская: <https://github.com/sofyaserpinskaya>
Frontend - Яндекс.Практикум

### Технологии

Python, Django, PostgreSQL, gunicorn, nginx, Docker.

### Шаблон наполнения env-файла

```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=secretkey
```

### Запуск проекта на сервере

Запуск контейнеров

```
sudo docker-compose up -d
```

Миграции

```
sudo docker-compose exec backend python manage.py migrate
```

Создание суперпользователя

```
sudo docker-compose exec backend python manage.py createsuperuser
```

Статика и загрузка данных в БД

```
sudo docker-compose exec backend python manage.py collectstatic
sudo docker-compose exec backend python manage.py load_data

```
