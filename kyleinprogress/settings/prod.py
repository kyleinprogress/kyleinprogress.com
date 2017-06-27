# settings/dev.py

from .common import *

ALLOWED_HOSTS = [
    'www.kyleinprogress.com',
    'kyleinprogress.com',
]

DEBUG = False

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

STATIC_ROOT = os.path.join(BASE_DIR, "static")
