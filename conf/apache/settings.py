import os
import sys

sys.path.append('/srv/www/dcmdb_dev')

os.environ['PYTHON_EGG_CACHE'] = '/srv/www/.python-egg'

os.environ['DJANGO_SETTINGS_MODULE'] = 'dicomdb.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
