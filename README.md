# Docker + API Template

`APITemplate`ning Docker versiyasi: User CRUD, kalkulyator (path/query) va qo'shimcha Category/Product CRUD. Ma'lumotlar bazasi PostgreSQL, server gunicorn, statik fayllar whitenoise orqali beriladi.

## Quick start

```bash
make run     # creates .venv and .env, installs deps, starts the app
make test    # checks + tests
```

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

- Health: http://127.0.0.1:8000/api/health/
- Kalkulyator: http://127.0.0.1:8000/api/calculator/path/5/7/ va http://127.0.0.1:8000/api/calculator/query/?n1=5&n2=7
- Userlar: http://127.0.0.1:8000/api/users/ (POST — ro'yxatdan o'tish, qolgani login bilan)
- Mahsulotlar: http://127.0.0.1:8000/api/categories/, http://127.0.0.1:8000/api/products/
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
make test
```

Eski versiyadan yangilaganda (custom User qo'shilgan) bazani bir marta qayta yarating: `docker compose down -v`.
