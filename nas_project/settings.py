"""
Django settings for nas_project project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
# This is crucial for local development secrets
load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------
# 🚨 SECURITY WARNINGS - FIXED FOR PRODUCTION
# -----------------------------------------------------------

# 1. SECRET_KEY: Loaded from environment. Fallback for quick local tests only.
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-kmld-f=z2jn0e_3vv*ah238lu2&xt50#_dfz%gyskcg)-_jvig'
)

# 2. DEBUG: Loaded from environment. Defaults to False for safety.
DEBUG = os.environ.get('DEBUG') == 'True' 

# 3. ALLOWED_HOSTS: Loaded from environment. Must be specific domains in production.
# Splits comma-separated values from the environment variable.
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 
    '127.0.0.1,localhost'
).split(',')

# -----------------------------------------------------------
# APPLICATION DEFINITION
# -----------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken', # Required for TokenAuthentication

    # Local apps
    'users.apps.UsersConfig', 
    'items.apps.ItemsConfig',
    'lending.apps.LendingConfig',
    'messaging',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Update SessionMiddleware for production performance if using Redis/Cache
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nas_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nas_project.wsgi.application'

# -----------------------------------------------------------
# DATABASE
# -----------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


# -----------------------------------------------------------
# STATIC & MEDIA FILES CONFIGURATION
# -----------------------------------------------------------

STATIC_URL = 'static/'
# STATIC_ROOT is essential for deployment (e.g., PythonAnywhere)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model Configuration
AUTH_USER_MODEL = 'users.User'

# -----------------------------------------------------------
# DJANGO REST FRAMEWORK (DRF) CONFIGURATION
# -----------------------------------------------------------

REST_FRAMEWORK = {
    # Sets default authentication to Token (for Postman/APIs) and Session (for browsable API)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication', 
        'rest_framework.authentication.SessionAuthentication',
    ],
    # Sets the default permission: requires login for almost all views
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # Forces date-time serialization to a standard format
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S%z",
    'DATE_FORMAT': "%Y-%m-%d",
}