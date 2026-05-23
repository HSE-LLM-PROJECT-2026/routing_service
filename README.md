# Routing Service

## Описание

Этот репозиторий содержит сервис управления логическими маршрутами и весами трафика. Сервис отделяет маршрутизацию от deployment lifecycle и работает с TrafficRoute CRD через Kubernetes client manager.

## Основные возможности
- создание traffic route для нескольких backend-развертываний
- просмотр текущей схемы маршрутизации
- обновление весов и состава backends
- отдельная ручка для release controller
- удаление маршрутов
- служебные health/livez/service-info ручки

## Структура проекта

- `app/` — основной код приложения
  - `main.py` — FastAPI-приложение и HTTP-ручки
  - `config.py` — настройки сервиса

- `deploy/` — файлы и переменные для развертывания
- `.env.example` — пример переменных окружения
- `Dockerfile` — сборка Docker-образа
- `pyproject.toml` — зависимости и настройки Python-проекта
- `requirements.txt` — список зависимостей для совместимого запуска без uv

## Быстрый старт локально

1. Установите зависимости:
   ```bash
   uv sync
   ```

2. Создайте `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Запустите сервис:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

Если `uv` не используется, можно запустить через обычный virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Переменные окружения
- `DATABASE_URL`
- `K8S_CLIENT_MANAGER_URL`
- `SECURITY_SERVICE_URL`
- `SERVICE_TOKEN`
- `LOG_LEVEL`

Пример `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/llm_platform
SERVICE_TOKEN=change-me
LOG_LEVEL=INFO
```

## Основные API-ручки

| Метод | Ручка | Назначение |
|--------|-------|------------|
| `GET` | `/health` | Проверяет доступность routing service. |
| `GET` | `/livez` | Liveness probe контейнера. |
| `GET` | `/service-info` | Отдает служебную информацию о routing service. |
| `GET` | `/traffic-routes` | Возвращает список логических маршрутов и текущие веса backend-развертываний. |
| `POST` | `/traffic-routes` | Создает TrafficRoute для двух и более deployment-объектов. |
| `GET` | `/traffic-routes/{alias}` | Возвращает конкретный маршрут по alias. |
| `PUT` | `/traffic-routes/{alias}` | Полностью обновляет состав backend-развертываний и веса маршрута. |
| `DELETE` | `/traffic-routes/{alias}` | Удаляет логический маршрут и связанный TrafficRoute CRD. |
| `POST` | `/traffic-routes/{alias}/weights` | Меняет только веса маршрута во время канареечного релиза. |
| `POST` | `/traffic-routes/{alias}/test` | Выполняет тестовый запрос через маршрут для проверки распределения трафика. |

## Сборка и запуск в Docker

```bash
docker build -t hse-llm-project-2026/routing_service:local .
docker run --env-file .env -p 8000:8000 hse-llm-project-2026/routing_service:local
```

## Деплой в Kubernetes

Файлы развертывания лежат в папке `deploy/`. Для сервисов, которые уже подключены к стенду, используются Helm values и deploy-скрипты из соответствующего репозитория или общего инфраструктурного пайплайна.

## Метрики и документация

- Swagger UI: `/docs`
- OpenAPI: `/openapi.json`
- Health check: `/health`
- Liveness check: `/livez`

## Автор

Igor Malysh
