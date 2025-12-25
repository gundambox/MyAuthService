"""
Development settings for myauthservice project.
This configuration is optimized for local development with console logging and debug mode enabled.
"""

import copy
import os

from .base import (
    AUTH_PASSWORD_VALIDATORS,
    BASE_DIR,
    DEFAULT_AUTO_FIELD,
    INSTALLED_APPS,
    LANGUAGE_CODE,
    LOGGING as BASE_LOGGING,
    MIDDLEWARE,
    ROOT_URLCONF,
    STATIC_URL,
    TEMPLATES,
    TIME_ZONE,
    USE_I18N,
    USE_TZ,
    WSGI_APPLICATION,
)

# Enable debug mode for development
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

SECRET_KEY = os.environ["SECRET_KEY"]

# Console logging configuration for development
# Extend base logging with oauth2 app-specific configuration
LOGGING = copy.deepcopy(BASE_LOGGING)
LOGGING["loggers"]["oauth2"] = {
    "handlers": ["console"],
    "level": "DEBUG",
    "propagate": False,
}

__all__ = [
    "ALLOWED_HOSTS",
    "AUTH_PASSWORD_VALIDATORS",
    "BASE_DIR",
    "DATABASES",
    "DEBUG",
    "DEFAULT_AUTO_FIELD",
    "INSTALLED_APPS",
    "LANGUAGE_CODE",
    "LOGGING",
    "MIDDLEWARE",
    "ROOT_URLCONF",
    "SECRET_KEY",
    "STATIC_URL",
    "TEMPLATES",
    "TIME_ZONE",
    "USE_I18N",
    "USE_TZ",
    "WSGI_APPLICATION",
]
