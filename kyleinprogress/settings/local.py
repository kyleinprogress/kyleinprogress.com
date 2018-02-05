# settings/dev.py

from .common import *

ALLOWED_HOSTS = [
    'www.kyleinprogress.local',
    'kyleinprogress.local',
]

DEBUG = True

# Jenkins Test Coverage
INSTALLED_APPS.append('django_jenkins')

JENKINS_TASKS = [
    'django_jenkins.tasks.run_pylint',
]

PROJECT_APPS = ['blog']

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR.joinpath('db.sqlite3')),
    }
}

# Django Development Toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False

INSTALLED_APPS.append('debug_toolbar')

INTERNAL_IPS = ['127.0.0.1', '192.168.10.1', '10.0.2.2']

MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.common.CommonMiddleware') + 1,
    'debug_toolbar.middleware.DebugToolbarMiddleware')
