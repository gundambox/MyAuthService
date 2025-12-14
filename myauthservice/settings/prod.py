"""
Production settings for myauthservice project.
This configuration is optimized for deployment in a production environment with security and performance considerations.
"""

import os
from .base import *


# Disable debug mode for production
DEBUG = False

# Define allowed hosts for production
if 'ALLOWED_HOSTS' not in os.environ:
    raise Exception("ALLOWED_HOSTS environment variable not set")
ALLOWED_HOSTS = [host.strip() for host in os.environ['ALLOWED_HOSTS'].split(',') if host.strip()]
if not ALLOWED_HOSTS:
    raise Exception("ALLOWED_HOSTS environment variable must contain at least one valid host")
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['PROD_DB_NAME'],
        'USER': os.environ['PROD_DB_USER'],
        'PASSWORD': os.environ['PROD_DB_PASSWORD'],
        'HOST': os.environ['PROD_DB_HOST'],
        'PORT': os.environ.get('PROD_DB_PORT', '3306'),
    }
}

SECRET_KEY = os.environ['SECRET_KEY']

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
    },
}

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True