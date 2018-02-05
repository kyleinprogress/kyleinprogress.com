#Settings for kyleinprogress project.

import json
import os
from pathlib import Path

# File Paths
PROJECT_PACKAGE = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_PACKAGE.parent

# Import Config.json
SECRETS = json.load(BASE_DIR.joinpath('config.json').open())

SECRET_KEY = str(SECRETS['secret_key'])

# Apps that are developed locally (home built)
LOCAL_APPS = [
    'blog',
]

# Third party apps installed from other people
THIRD_PARTY_APPS = [
    'markdown2',
    'copyright',
]

# Django default applications
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.syndication',

]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DEFAULT_APPS

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'kyleinprogress.urls'

SITE_ID = 3

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(PROJECT_PACKAGE.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]



WSGI_APPLICATION = 'kyleinprogress.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [str(PROJECT_PACKAGE.joinpath('static'))]

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR.joinpath('m'))


# Django Copyright
COPY_START_YEAR = 2016
