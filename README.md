# Docker API Template

A Dockerized Django REST Framework starter: Postgres, gunicorn, WhiteNoise and
OpenAPI docs, wired together with Docker Compose.

## Stack

- Django 6.1 + Django REST Framework 3.18
- PostgreSQL 16 (Compose service)
- drf-spectacular (OpenAPI 3 + Swagger UI)
- gunicorn + WhiteNoise
- django-environ (settings read from `.env`)

## Getting started

```bash
cp .env.example .env          # then set SECRET_KEY

docker compose up --build
```

The entrypoint waits for Postgres, then runs `migrate` and `collectstatic`
before starting the server. The API is served at http://localhost:8000

Without Docker:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

## Endpoints

| Path | Description |
|---|---|
| `/api/schema/` | OpenAPI 3 schema |
| `/api/docs/` | Swagger UI |
| `/admin/` | Django admin |

## Layout

```
dockerapitemplate/   # project settings, urls, wsgi/asgi
apps/                # the API app
Dockerfile           # application image
docker-compose.yml   # web + Postgres services
entrypoint.sh        # waits for Postgres, migrates, collects static
```

## Environment variables

See `.env.example`: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, the `POSTGRES_*`
credentials and `DATABASE_URL`.
