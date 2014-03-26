DEBUG = True

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "dcmdb",
    "USER": "dcmdb",
    "PASSWORD": "milka123",
    "HOST": "localhost"
  }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = 'neurosnap@gmail.com'
EMAIL_PASS = 'Sodone123'