"""
Django settings for pollme project.
Updated for Django 5.2.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Use modern pathlib for path management.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Core Security Settings ---

# SECURITY WARNING: keep the secret key used in production secret!
# It's a best practice to load this from an environment variable.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'x*za6xf&_80ofdpae!yzq61g9ffikkx9$*iygbl$j7rr4wlf8t')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# For development, '*' is fine. For production, be specific.
ALLOWED_HOSTS = ["*"]


# --- Application Definition ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pollme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Use pathlib for defining the project-level templates directory.
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'pollme.wsgi.application'


# --- Database Configuration ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Use pathlib for the database path.
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC' # Changed from Asia/Dhaka for better timezone handling with USE_TZ=True
USE_I18N = True
USE_TZ = True
# REMOVED: USE_L10N was removed in Django 5.0 and will cause an error.


# --- Static & Media Files ---
STATIC_URL = '/static/'
# Directory where Django can find your project's static files.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# Directory where 'collectstatic' will place all files for production.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# For user-uploaded files (e.g., images).
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- Default Primary Key Field Type ---
# This is now a standard setting in modern Django projects.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'