import os

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '5432',
    }
}

STATIC_URL = os.environ['STATIC_URL']
MEDIA_URL = os.environ['MEDIA_URL']

EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASS  WORD']
URL_FOR_CHANGE_AUTH_DATA = os.environ['URL_FOR_CHANGE_AUTH_DATA']

if os.environ.get('OFF_CSRF_AND_COOKIE_SECURE'):
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

STATS_CACHE_TIMEOUT = 60
STATS_CACHE_UPDATE_TIMEOUT = 0
