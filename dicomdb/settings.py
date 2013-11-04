import os
# current directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# where media files get downloaded to
MEDIA_ROOT = BASE_DIR + '/media'
# where all the static files get dumped
STATIC_ROOT = BASE_DIR + '/static/'
STATIC_URL = '/static/'

ROOT_URLCONF = 'dicomdb.urls'
WSGI_APPLICATION = 'dicomdb.wsgi.application'

import socket
HOST = socket.gethostname()

# EASY FLAG TO REMOVE URLS AND PUSH SITE INTO DEVELOPMENT
#SITE_STATE = "dev"
SITE_STATE = "live"

#production
if HOST == "dcmdb.org":

    try:
        from settings_prod import *
    except ImportError:
        pass

    ALLOWED_HOSTS = ['54.200.118.134']

#development
else:

    try:
        from settings_dev import *
    except ImportError:
        pass

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    BASE_DIR + "/templates/",
    BASE_DIR + "/main/templates/",
    BASE_DIR + "/users/templates/",
    BASE_DIR + "/dcmview/templates",
    BASE_DIR + "/dcmupload/templates",
)

# Additional locations of static files
STATICFILES_DIRS = (
    BASE_DIR + '/templates/static/',
    BASE_DIR + '/main/static/',
    BASE_DIR + '/users/static/',
    BASE_DIR + "/dcmview/static/",
    BASE_DIR + "/dcmupload/static/",
)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
