SHELL := /bin/bash
PY := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python

DJANGO_SETTINGS_MODULE := myauthservice.settings.dev

.PHONY: help dev setup install migrate run clean

help:
	@echo "Targets:"
	@echo "  make dev      - one command to start dev server"
	@echo "  make setup    - create venv + install deps + migrate"
	@echo "  make clean    - remove venv"

dev: setup run

setup: $(VENV) install migrate

$(VENV):
	$(PY) -m venv $(VENV)

install:
	$(PIP) install -r requirements.txt

migrate:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) $(PYTHON) manage.py migrate

run: $(VENV) install migrate
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) $(PYTHON) manage.py runserver 0.0.0.0:8000

clean:
	rm -rf $(VENV)
