from __future__ import print_function
import os
from django.utils.crypto import get_random_string
import socket

# current directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# where media files get downloaded to
MEDIA_ROOT = BASE_DIR + '/media/'
# where all the static files get dumped
STATIC_ROOT = BASE_DIR + '/static/'
STATIC_URL = '/static/'

ROOT_URLCONF = 'dicomdb.urls'
WSGI_APPLICATION = 'dicomdb.wsgi.application'

HOST = socket.gethostname()

# EASY FLAG TO REMOVE URLS AND PUSH SITE INTO DEVELOPMENT
#SITE_STATE = "dev"
SITE_STATE = "live"

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

# EMAIL SETTINGS
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

def generate_secret_key(filename):

	chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
	key = get_random_string(50, chars)
	key_contents = "SECRET_KEY = '" + key + "'"

	f = open(filename,'w')
	print(key_contents, file = f)

#override default settings in these files
#production
if HOST == "dcmdb.org":

	try:
		from settings_prod import *
	except ImportError:
		pass

	DEBUG = False

	#user for email primarily
	DOMAIN = HOST

#development
else:

	try:
		from settings_dev import *
	except ImportError:
		pass

	DEBUG = True

	#user for emails primarily
	DOMAIN = "127.0.0.1:8000"

#On fresh clone, no secret_key.py exists so automate the generation
#user executing django will need write access for this to work
#properly, or one can simply generate a one-time key using the same script
try:

	from secret_key import *

except ImportError:

	#get path of settings directory
	SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
	#generate a new django secret key
	generate_secret_key(os.path.join(SETTINGS_DIR, 'secret_key.py'))

	from secret_key import *
