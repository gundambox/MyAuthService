# Read Me

## Introduction

This project is a bootstrap/scaffolding setup for a Django authentication service. It is primarily a personal side project built to learn OAuth 2.0 by implementing an OAuth 2.0 authorization server step by step, and to document the design decisions and trade-offs along the way.

The repository currently focuses on establishing a solid development foundation (project structure, settings split, local workflow). OAuth 2.0 functionality and related endpoints will be introduced incrementally in future PRs.

## Requirements

- Python 3.12+
- [`pip`](https://pip.pypa.io/en/stable/) for dependency management
- pkg-config
- libmysqlclient-dev

## Installation

```bash
pip install -r requirements.txt
```

## Local Development

### Start (one command)

```bash
make dev
```

### What it does

- Create venv at `.venv/`
- Install dependencies from `requirements.txt`
- Run `python manage.py migrate`
- Start Django dev server at `http://localhost:8000`

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
    # Run server with dev settings
    DJANGO_SETTINGS_MODULE=myauthservice.settings.dev python manage.py runserver

    # Run tests with test settings
    DJANGO_SETTINGS_MODULE=myauthservice.settings.test python manage.py test
    ```
2. **By using the `--settings` command-line option with `manage.py` commands:**
    ```bash
    # Run server with dev settings
    python manage.py runserver --settings=myauthservice.settings.dev

    # Run tests with test settings
    python manage.py test --settings=myauthservice.settings.test
    ```

## Running Tests
- To run tests:
  ```bash
  pytest tests/
  ```

## Linting and Formatting
- To run lint checks:
  ```bash
  flake8 .
  ```
- To auto-format code:
  ```bash
  black .
  ```

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

## API Endpoints

The API is accessible under the `/api/` prefix.

### Health Check

Check if the service is running and healthy.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

**Example:**
```bash
curl http://localhost:8000/api/health
```

### Version (Optional)

Get service name and version information.

**Endpoint:** `GET /api/version`

**Response:**
```json
{
  "service": "MyAuthService",
  "version": "0.1.0"
}
```