import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'admin',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': ''
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'