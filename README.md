# Routing Service

## Описание

Сервис маршрутизации трафика между deployment-бэкендами и управления весами маршрутов.

## Основные возможности

- создание и изменение TrafficRoute
- удаление маршрутов
- изменение весов и тест маршрута

## Структура проекта

- `app/` - код сервиса (FastAPI, config, domain handlers)
- `deploy/` - служебные файлы для роли сервиса в деплое
- `pyproject.toml` - зависимости и метаданные проекта
- `Dockerfile` - сборка контейнера
- `.env.example` - пример переменных окружения

## Быстрый старт (локально)

1. Установить зависимости:
   `uv sync --frozen --extra dev`
2. Запустить сервис:
   `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Проверить health:
   `curl http://127.0.0.1:8000/health`

## Переменные окружения

- `SERVICE_ROLE` - роль сервиса в control plane
- `SERVICE_NAME` - техническое имя сервиса
- `POSTGRES_DSN` - строка подключения к PostgreSQL
- `PROMETHEUS_BASE_URL` - адрес Prometheus
- `SERVICE_TO_SERVICE_URLS_JSON` - карта внутренних URL сервисов

## Docker

- Сборка: `docker build -t routing_service:local .`
- Запуск: `docker run --rm -p 8000:8000 --env-file .env routing_service:local`

## Деплой

Файлы для деплоя лежат в `deploy/`.

## Основные API ручки

- `GET /traffic-routes`
- `POST /traffic-routes`
- `GET /traffic-routes/{alias}`
- `PUT /traffic-routes/{alias}`
- `DELETE /traffic-routes/{alias}`
- `POST /traffic-routes/{alias}/weights`
- `POST /traffic-routes/{alias}/test`
