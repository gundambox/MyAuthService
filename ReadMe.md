# Read Me

## Introduction

This project is a bootstrap/scaffolding setup for a Django authentication service using JWT (JSON Web Tokens). Endpoints for user registration, login, and token validation are planned but not yet implemented.

## Requirements

- Python 3.x
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

Local development uses a .env file (not committed). Copy .env.example to .env and set required variables.

### Required

- `SECRET_KEY`: A long, random string for Django's secret key.

Example:

```bash
cp .env.example .env
# edit .env and set SECRET_KEY
SECRET_KEY=your-long-random-secret
```

> **Notes:**
> - `.env` is for local development only.
> - In production, do not rely on `.env`; inject environment variables via your deployment platform.

## Settings (dev / prod / test)

Settings are split into modules under `myauthservice/settings/`:

* `base.py`: common settings
* `dev.py`: development settings (console logging)
* `prod.py`: production settings (should be strict / fail-fast)
* `test.py`: test settings (isolated + faster)

### Run with specific settings

You can specify which settings module to use in two ways:

1. **By setting the `DJANGO_SETTINGS_MODULE` environment variable (this overrides the default in `manage.py`):**

   ```bash
   DJANGO_SETTINGS_MODULE=myauthservice.settings.dev python manage.py runserver
   DJANGO_SETTINGS_MODULE=myauthservice.settings.test python manage.py test
## Logging

* Development logging writes to console (stdout).
* Production/staging should prefer stdout logging and let the platform collect logs.

## Project structure

This repository contains a Django + Django REST Framework project scaffold for an OAuth 2.0 authorization server. OAuth 2.0 functionality is planned for future PRs.

```text
.
├── ReadMe.md
├── manage.py               # Django management script
├── myauthservice           # Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings
│   │   ├── __init__.py
│   │   ├── base.py         # common settings
│   │   ├── dev.py          # development settings
│   │   ├── prod.py         # production settings
│   │   └── test.py         # testing settings
│   ├── urls.py
│   └── wsgi.py
├── oauth2                  # Django app for OAuth 2.0 implementation
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── requirements.txt        # Project dependencies
└── tests                   # Test suite
    ├── __init__.py
    └── test_smoke.py
```