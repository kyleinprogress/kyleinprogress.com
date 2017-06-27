 settings/dev.py

from .common import *

ALLOWED_HOSTS = [
    'test.kyleinprogress.net',
]

DEBUG = True

# Jenkins Test Coverage
THIRD_PARTY_APPS.append('django_jenkins')

JENKINS_TASKS = [
    'django_jenkins.tasks.run_pylint',
]

PROJECT_APPS = ['blog']

# Database Connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kyleinprogress_django_test',
        'USER': SECRETS.get('db_user', ''),
        'PASSWORD': SECRETS.get('db_password', ''),
        'HOST': SECRETS.get('db_host', ''),
    }
}
