from __future__ import print_function
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = BASE_DIR + '/media/'
STATIC_ROOT = BASE_DIR + '/static/'
STATIC_URL = '/static/'

ROOT_URLCONF = 'dcmdb.urls'
WSGI_APPLICATION = 'dcmdb.wsgi.application'

# EASY FLAG TO REMOVE URLS AND PUSH 
# SITE INTO UNDER CONSTRUCTION
UNDER_CONSTRUCTION = False
DEBUG = False
#used for email primarily
DOMAIN = "dcmdb.org"

#TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
	BASE_DIR + "/templates/",
	BASE_DIR + "/main/templates/",
	BASE_DIR + "/users/templates/",
	BASE_DIR + "/dcmview/templates",
	BASE_DIR + "/uploader/templates",
)

STATICFILES_DIRS = (
	BASE_DIR + '/templates/static/',
	BASE_DIR + '/main/static/',
	BASE_DIR + '/users/static/',
	BASE_DIR + "/dcmview/static/",
	BASE_DIR + "/uploader/static/",
)

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
	'uploader',
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#override default settings in these files
try:
	from settings_env import *
except ImportError:
	pass

def generate_secret_key(filename):

	from django.utils.crypto import get_random_string

	chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
	key = get_random_string(50, chars)
	key_contents = "SECRET_KEY = '" + key + "'"

	f = open(filename,'w')
	print(key_contents, file = f)

#On fresh clone, no secret_key.py exists so automate the generation
#user executing django will need write access for this to work
#properly, or one can simply generate a one-time key using the same script
try:
	from secret_key import *
except ImportError:
	SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
	generate_secret_key(os.path.join(SETTINGS_DIR, 'secret_key.py'))

	from secret_key import *