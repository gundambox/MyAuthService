"""
Testing settings for MyAuthService project.
This configuration is optimized for running tests with an in-memory database.
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
    REST_FRAMEWORK,
    ROOT_URLCONF,
    SERVICE_VERSION,
    STATIC_URL,
    TEMPLATES,
    TIME_ZONE,
    USE_I18N,
    USE_TZ,
    WSGI_APPLICATION,
)

# Enable debug mode during tests to provide detailed error messages and stack traces.
# This helps diagnose test failures, but should not be used in production.
DEBUG = True

# Allow all hosts during testing to prevent host header validation errors in test environments and CI pipelines
ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

SECRET_KEY = os.environ["SECRET_KEY"]

# Console logging configuration for testing.
#
# By default, tests should run quietly to avoid cluttering test output.
# However, verbose logging is enabled here to assist with debugging test failures
# and to provide detailed information when diagnosing issues in CI environments.
# If less verbosity is desired, consider switching the formatter to 'simple'
# and raising the log level to 'WARNING' or higher.
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
    "REST_FRAMEWORK",
    "ROOT_URLCONF",
    "SECRET_KEY",
    "SERVICE_VERSION",
    "STATIC_URL",
    "TEMPLATES",
    "TIME_ZONE",
    "USE_I18N",
    "USE_TZ",
    "WSGI_APPLICATION",
]
