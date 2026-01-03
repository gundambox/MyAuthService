# MyAuthService

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

MyAuthService is a Django-based OAuth 2.0 authorization server built for learning and experimentation. This project serves as a practice implementation of OAuth 2.0 protocols, focusing on proper architecture, testing practices, and documentation.

**Current Status:** Bootstrap/scaffolding phase. OAuth 2.0 endpoints and functionality will be introduced incrementally in future releases.

## Technology Stack

- Python 3.12+
- Django 6.0+
- Django REST Framework
- MySQL (production) / SQLite (development)
- Docker & Docker Compose
- pytest for testing

## Prerequisites

- Docker
- Docker Compose
- Git

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/gundambox/MyAuthService.git
cd MyAuthService
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and set required variables:

```bash
SECRET_KEY=your-long-random-secret-key-here
```

Generate a secure `SECRET_KEY`:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Build and Start Services

```bash
make build
make up
```

### 4. Run Migrations

```bash
make migrate
```

### 5. Verify Installation

```bash
make test
```

The application will be available at `http://localhost:8000`

## Common Commands

### Container Management

```bash
make up         # Start services
make down       # Stop services
make down-v     # Stop services and remove volumes (reset database)
make logs       # View container logs
make shell      # Access container shell
```

### Database Operations

```bash
make migrate    # Run database migrations
```

### Testing

```bash
make test       # Run all tests
```

Run specific tests:

```bash
docker compose run --rm -e DJANGO_SETTINGS_MODULE=myauthservice.settings.test app pytest tests/integration/test_health_endpoint.py
```

### Code Quality

Format code:

```bash
make shell
black .
exit
```

Lint code:

```bash
make shell
flake8 .
exit
```

Or run directly:

```bash
docker compose exec app black .
docker compose exec app flake8 .
```

## Settings Configuration

Settings are split into environment-specific modules under `myauthservice/settings/`:

- `base.py` - Common settings
- `dev.py` - Development settings (SQLite, debug enabled)
- `test.py` - Test settings (in-memory SQLite)
- `prod.py` - Production settings (MySQL, security hardened)

Specify settings module:

```bash
DJANGO_SETTINGS_MODULE=myauthservice.settings.dev python manage.py runserver
```

Or:

```bash
python manage.py runserver --settings=myauthservice.settings.dev
```

## API Endpoints

### API Documentation

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- OpenAPI Schema: `http://localhost:8000/schema/`

## Versioning

Service version is managed via the `VERSION` file in the project root.

### Version Format

Semantic versioning: `major.minor.patch`

| Change Type | Version Update | Reset |
|-------------|----------------|-------|
| Breaking change / Feature removal | `major + 1` | `minor = 0`, `patch = 0` |
| New feature | `minor + 1` | `patch = 0` |
| Bug fix / Documentation / Chore | `patch + 1` | - |

### Examples

- `0.1.0` → `1.0.0` (breaking change)
- `0.1.0` → `0.2.0` (new feature)
- `0.1.0` → `0.1.1` (bug fix)

### Version Endpoint

```bash
curl http://localhost:8000/api/version/
```

Response:

```json
{
  "service": "MyAuthService",
  "version": "0.1.2"
}
```

## Project Structure

```
.
├── myauthservice/          # Django project
│   ├── settings/           # Environment-specific settings
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── test.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── oauth2/                 # OAuth 2.0 app
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── tests/                  # Test suite
│   ├── test_smoke.py
│   └── integration/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── VERSION
```

## Environment Variables

### Required

- `SECRET_KEY` - Django secret key (minimum 50 characters)

### Optional

- `DJANGO_LOG_LEVEL` - Logging level (default: INFO)
- `DEBUG` - Enable debug mode (default: False in production)
- `ALLOWED_HOSTS` - Comma-separated allowed hosts

### Production Only

- `PROD_DB_NAME` - Database name
- `PROD_DB_USER` - Database user
- `PROD_DB_PASSWORD` - Database password
- `PROD_DB_HOST` - Database host
- `PROD_DB_PORT` - Database port (default: 3306)

## Contributing

This is a solo learning project. For development workflow and guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

For security concerns, see [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
