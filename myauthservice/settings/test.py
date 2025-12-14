"""
Testing settings for MyAuthService project.
This configuration is optimized for running tests with an in-memory database.
"""

import os
from .base import *

# Enable debug mode during tests to provide detailed error messages and stack traces.
# This helps diagnose test failures, but should not be used in production.
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

if 'SECRET_KEY' not in os.environ:
    raise Exception("SECRET_KEY environment variable not set")
SECRET_KEY = os.environ['SECRET_KEY']

# Console logging configuration for testing
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}][{levelname}][{process:d}][{thread:d}][{filename}:{lineno}] - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'oauth2': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}