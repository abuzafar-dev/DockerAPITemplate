# Docker + API Template

Django REST Framework API shablonining Docker versiyasi. Ma'lumotlar bazasi PostgreSQL, server gunicorn, statik fayllar whitenoise orqali beriladi.

## Docker bilan ishga tushirish

```bash
cp .env.example .env
docker compose up --build
```

Konteyner ishga tushganda `migrate` va `collectstatic` avtomatik bajariladi.

Superuser yaratish:

```bash
docker compose exec web python manage.py createsuperuser
```

- API: http://127.0.0.1:8000/api/products/
- Swagger: http://127.0.0.1:8000/api/docs/
- Admin: http://127.0.0.1:8000/admin/

## Dockersiz ishga tushirish

`.env` faylida `POSTGRES_DB` bo'lmasa loyiha SQLite bilan ishlaydi.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Testlar

```bash
docker compose exec web python manage.py test
```
