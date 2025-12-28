SHELL := /bin/bash

COMPOSE := docker compose
SERVICE := app

.PHONY: help up down down-v build logs shell migrate test

help:
	@echo "Docker Compose targets:"
	@echo "  make up       - docker: up -d"
	@echo "  make down     - docker: down"
	@echo "  make down-v   - docker: down -v (reset volumes)"
	@echo "  make build    - docker: build"
	@echo "  make logs     - docker: logs -f"
	@echo "  make shell    - docker: exec bash in $(SERVICE)"
	@echo "  make migrate  - docker: run migrations"
	@echo "  make test     - docker: run pytest with test settings"

up:
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

down:
	$(COMPOSE) down

down-v:
	$(COMPOSE) down -v

logs: up
	$(COMPOSE) logs -f $(SERVICE)

shell: up
	$(COMPOSE) exec $(SERVICE) bash

migrate:
	$(COMPOSE) exec $(SERVICE) python manage.py migrate

test:
	$(COMPOSE) run --rm -e DJANGO_SETTINGS_MODULE=myauthservice.settings.test $(SERVICE) pytest
