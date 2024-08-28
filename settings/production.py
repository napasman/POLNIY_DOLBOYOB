from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.teleteg.com','teleteg.com', 'http://test-tele111.herokuapp.com', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'teleteg',
        'USER': 'alex',
        'PASSWORD': "admin1234",
        'HOST': 'localhost'
    }
}

'''
