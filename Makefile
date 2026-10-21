.PHONY: help install run test down logs

help:
	@echo "make run      — Docker'da ishga tushirish (http://127.0.0.1:8000/api/docs/)"
	@echo "make down     — to'xtatish"
	@echo "make logs     — loglar"
	@echo "make test     — testlar (Docker'siz)"

run: .env
	@echo "==> http://127.0.0.1:8000/api/docs/"
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

PY := .venv/bin/python

.venv/bin/python:
	@if command -v uv >/dev/null 2>&1; then uv venv -q --python 3.12 .venv; else python3 -m venv .venv; fi

.venv/.installed: requirements.txt | .venv/bin/python
	@echo "==> kutubxonalar o'rnatilmoqda"
	@if command -v uv >/dev/null 2>&1; then uv pip install -q -p $(PY) -r requirements.txt; else $(PY) -m pip install -q -r requirements.txt; fi
	@touch $@

install: .venv/.installed

.env:
	@cp .env.example .env
	@sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')|" .env
	@echo "==> .env yaratildi (.env.example asosida)"

test: install
	@bash scripts/ci.sh
