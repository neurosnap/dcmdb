# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import socket
HOST = socket.gethostname()

#production
if HOST == "dcmdb.org":
    try:
        from settings_prod import *
    except ImportError:
        pass
#development
else:
    try:
        from settings_dev import *
    except ImportError:
        pass


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vd0pm=vq2&3x@xlx=e&(bg37ovt#x=je=vu0l3g@ljf#d26a73'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    BASE_DIR + "/templates/",
    BASE_DIR + "/main/templates/",
    BASE_DIR + "/users/templates/",
    BASE_DIR + "/dcmview/templates",
    BASE_DIR + "/dcmupload/templates",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATIC_ROOT = BASE_DIR + '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    BASE_DIR + '/templates/static/',
    BASE_DIR + '/main/static/',
    BASE_DIR + '/users/static/',
    BASE_DIR + "/dcmview/static/",
    BASE_DIR + "/dcmupload/static/",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'

ALLOWED_HOSTS = ['54.200.118.134']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'main',
    'users',
    'dcmview',
    'dcmupload',
    'down',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dicomdb.urls'

WSGI_APPLICATION = 'dicomdb.wsgi.application'

MEDIA_ROOT = BASE_DIR + '/media'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# Check for production environment

DATABASES = {
    'default': SETTINGS_DB
}

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = SETTINGS_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = SETTINGS_EMAIL_PASS
EMAIL_PORT = 587

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
