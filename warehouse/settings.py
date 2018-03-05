"""
Django settings for warehouse project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wn3j9y%z)6cic3c#$$p9#3_*b+#zk(e0r)^i#qo8lntdjez(xl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'warehouse',
    'warehouse.markets',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'warehouse.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'warehouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


import os
IS_PRODUCTION = os.environ.get('IS_PRODUCTION', False) == 'true'
DATABASE_PORT = '5432'
DATABASE_NAME = 'cryptodb'
DATABASE_HOST = os.environ.get('DATABASE_URL')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if IS_PRODUCTION:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


from crypto_mediator import CryptoMediator

from crypto_mediator.secret import (
    BITTREX_API_KEY, BITTREX_API_SECRET,
    COINBASE_API_KEY, COINBASE_API_SECRET,
    GATECOIN_API_KEY, GATECOIN_API_SECRET,
    GDAX_API_KEY, GDAX_API_SECRET, GDAX_PASSPHRASE,
    LIQUI_API_KEY, LIQUI_API_SECRET,
    POLONIEX_API_KEY, POLONIEX_API_SECRET,
)

kwargs = {
    'liqui': {'key': LIQUI_API_KEY, 'secret': LIQUI_API_SECRET},
    # 'poloniex': {'key': POLONIEX_API_KEY, 'secret': POLONIEX_API_SECRET},
    # 'bittrex': {'api_key': BITTREX_API_KEY, 'api_secret': BITTREX_API_SECRET},
    # 'coinbase': {'api_key': COINBASE_API_KEY, 'api_secret': COINBASE_API_SECRET},
    # 'gdax': {'key': GDAX_API_KEY, 'b64secret': GDAX_API_SECRET, 'passphrase': GDAX_PASSPHRASE},
    # 'gatecoin': {'key': GATECOIN_API_KEY, 'secret': GATECOIN_API_SECRET},
}

METACLIENT = CryptoMediator(**kwargs)

