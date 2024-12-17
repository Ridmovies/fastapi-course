# Fastapi Cервис My_booking
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Асинхронность](https://img.shields.io/badge/-Асинхронность-464646?style=flat-square&logo=Асинхронность)]()
[![Anyio](https://img.shields.io/badge/-Anyio-464646?style=flat-square&logo=Anyio)](https://anyio.readthedocs.io/en/stable/)
[![Cookies](https://img.shields.io/badge/-Cookies-464646?style=flat-square&logo=Cookies)]()
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat-square&logo=JWT)]()
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)](https://redis.io/)
[![Celery](https://img.shields.io/badge/-Celery-464646?style=flat-square&logo=Celery)](https://docs.celeryq.dev/en/stable/)
[![Sentry](https://img.shields.io/badge/-Sentry-464646?style=flat-square&logo=Sentry)](https://sentry.io/welcome/)
[![Prometheus](https://img.shields.io/badge/-Prometheus-464646?style=flat-square&logo=Prometheus)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/-Grafana-464646?style=flat-square&logo=Grafana)](https://grafana.com/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat-square&logo=uvicorn)](https://www.uvicorn.org/)
[![Gunicorn](https://img.shields.io/badge/-Gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

Cервис бронирования отелей.Пользователи могут забронировать необходимый тип номера в отеле на определённую дату.

## Доступный функционал


## Инструменты в проекте:
* Python 3.12
* fastapi==0.115.6
* postgresql+asyncpg
* SQLAlchemy==2.0.36
* alembic==1.14.0
* Jinja2
* Redis
* fastapi-cache2
* Celery
* Flower
* SQLAlchemy Admin


## Установка

Запустить проект
```bash
uvicorn main:app --reload
```

```bash
python main.py
```

### Требования

Список необходимых зависимостей и программного обеспечения.

### Установка зависимостей

Команды для установки зависимостей.

### Настройка

Шаги для настройки проекта перед запуском.

## Запуск

Инструкции по запуску проекта.

### Локальный запуск

Команды для запуска проекта локально.

### Развертывание

Рекомендации по развертыванию проекта в продакшн-среду.

## Документация

Ссылки на документацию API и другие полезные ресурсы.

## Лицензия

Информация о лицензии проекта.


## Development

### Alembic

### Создайте директорию для хранения конфигурационных файлов и скриптов миграции:
```bash
alembic init migrations
```

### Генерация первой миграции
```bash
alembic revision --autogenerate -m "initial migration"
```

### Примените созданную миграцию к базе данных:
```bash
alembic upgrade head
```

### Откат миграции
```bash
alembic downgrade -1
```
Где -1 означает откат на одну версию назад. Можно указать конкретную ревизию, до которой нужно откатиться.


### Сброс базы данных
Если вы хотите сбросить базу данных до начального состояния, выполните:
```bash
alembic downgrade base
```


### Импорт CSV-файла

Используем команду COPY для загрузки данных из CSV-файла в таблицу rooms. Для этого необходимо иметь доступ к серверу базы данных и возможность копирования файла на сервер.

#### Копирование локального CSV-файла

Если CSV-файл находится на том же компьютере, что и клиент PostgreSQL, можно использовать следующую команду:

```SQL
COPY rooms(name, description, price_per_day, services, quantity, hotel_id, image_id)
FROM '/path/to/your/file.csv' DELIMITER ';' CSV HEADER;
```

#### Копирование удаленного CSV-файла

Если CSV-файл находится на другом сервере, можно использовать команду \copy в psql:

```bash
psql -U postgres -d booking_db -c "\copy rooms(name, description, price_per_day, services, quantity, hotel_id, image_id) FROM '/path/to/your/file.csv' DELIMITER ';' CSV HEADER;"
```

## Команды для работы с Celery
### Запуск рабочего процесса
```bash
celery -A app.tasks.tasks:celery worker -l INFO
```
app.tasks.tasks:celery - Это путь до экземпляра Celery()

### Запуск планировщика
To start the celery beat service:
```bash
celery -A store beat -l INFO
```

### Запустить Flower
```bash
celery -A app.tasks.tasks:celery flower
```
веб-интерфейс: http://0.0.0.0:5555/


## Линтеры и форматеры:
```bash
black --check --diff --color ./app/booking/services.py
```

```bash
isort --check-only --diff --profile black ./app/booking/services.py
```

```bash
mypy --incremental ./product_app/views.py 
```

```bash
autoflake ./app/booking/router.py
```

```bash
pyright .
```