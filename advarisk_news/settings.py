from .base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'advarisk_news',
        'USER': 'postgres',
        'PASSWORD': 'shantam123',
        'HOST': 'localhost',
        'PORT': '',
    }
}
