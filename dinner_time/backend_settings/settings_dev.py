import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '5432' if not os.environ.get('DB_PORT') else os.environ['DB_PORT'],
    }
}

STATIC_URL = '/staticfiles/'
MEDIA_URL = '/media/'

if os.environ.get('OFF_CSRF_AND_COOKIE_SECURE'):
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

STATS_CACHE_TIMEOUT = 60
STATS_CACHE_UPDATE_TIMEOUT = 0

EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

URL_FOR_CHANGE_AUTH_DATA = os.environ['URL_FOR_CHANGE_AUTH_DATA']