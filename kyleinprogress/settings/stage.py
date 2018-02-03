# settings/dev.py

from .common import *

ALLOWED_HOSTS = [
    'test.kyleinprogress.net',
]

DEBUG = True

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

STATIC_ROOT = os.path.dirname(BASE_DIR) + '/public/static/'
