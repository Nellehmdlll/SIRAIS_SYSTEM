"""
Django settings for SIRAIS project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from .juzmin import JAZZMIN_SETTINGS
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)=*88au@t*wvtvz^!e5!q50e*y95r))0++4za*ln0yrf#8=bg8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.ModelBackend', 
)

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sirais_app',
    'sslserver',
    
    
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

ROOT_URLCONF = 'SIRAIS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'static',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sirais_app.context_processors.disponibleProject',
                'sirais_app.context_processors.active_project',

                
            ],
        },
    },
]

WSGI_APPLICATION = 'SIRAIS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} 
 
""" 
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'bd_sirais',
    'USER': 'root',
    'PASSWORD': '',
    'HOST':'localhost',
    'PORT':'3306',
    }
}
"""
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "sirais_app/static"]

MEDIA_URL = '/image/'
MEDIA_ROOT = os.path.join(BASE_DIR, "sirais_app/static/image")


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'sirais_app.CustomUser'  

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  

CRISPY_TEMPLATE_PACK = 'bootstrap4'

JAZZMIN_SETTINGS = JAZZMIN_SETTINGS

GOOGLE_CALENDAR_CLIENT_ID = '568216439187-iuct59qehu691etdgv9is8rmihk59ace.apps.googleusercontent.com'
GOOGLE_CALENDAR_CLIENT_SECRET = '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'
GOOGLE_CALENDAR_REDIRECT_URI = 'http://localhost:8000/oauth2callback/'
# LOGIN_REDIRECT_URL = reverse_lazy('google_auth_return')
# LOGOUT_REDIRECT_URL ='/'

 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'