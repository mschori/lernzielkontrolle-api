import datetime
import os
from pathlib import Path

import dj_database_url
import django_heroku
import environ

# Project-Version
PROJECT_VERSION = '1.0.0'

# Initialize Environment-Variables
env = environ.Env()
environ.Env.read_env('.env')

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = env('SECRET_KEY')

# Debug-Mode
DEBUG = env('DEBUG') == '1' or env('DEBUG') == 'True'

# Allowed Hosts
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'users',
    'drf_auth',
    'learn_aim_check'
]

# Middleware definition
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL Configuration
ROOT_URLCONF = 'tie_athena.urls'

# Template Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-Application
WSGI_APPLICATION = 'tie_athena.wsgi.application'

# Database --> Parse Database-URL if available
if "DATABASE_URL" in os.environ:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Forwarding HTTP to HTTPS
if env('ENABLE_HTTPS_REDIRECT') == '1' or env('ENABLE_HTTPS_REDIRECT') == 'True':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Heroku Settings
django_heroku.settings(locals())

# Django Rest-Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Simple-JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=20) if DEBUG else datetime.timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=25) if DEBUG else datetime.timedelta(days=5),
}

# CORS Configuration
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = tuple(os.environ.get('CORS_ORIGIN_WHITELIST').split(','))
