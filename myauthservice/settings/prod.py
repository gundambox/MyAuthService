"""
Production settings for myauthservice project.
This configuration is optimized for deployment in a production environment with security and performance considerations.
"""

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

# Validate required database environment variables
required_db_vars = ['PROD_DB_NAME', 'PROD_DB_USER', 'PROD_DB_PASSWORD', 'PROD_DB_HOST']
missing_vars = [var for var in required_db_vars if var not in os.environ]
if missing_vars:
    raise Exception(f"Required database environment variables not set: {', '.join(missing_vars)}")

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

# Use base logging configuration
# Production uses the same logging configuration as base
LOGGING = BASE_LOGGING

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True