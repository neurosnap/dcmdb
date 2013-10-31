import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SETTINGS_DB = {
	"ENGINE": "django.db.backends.sqlite3",
	"NAME": os.path.join(BASE_DIR, "db.sqlite3")
}

SECRET_KEY = 'vd0pm=vq2&3x@xlx=e&(bg37ovt#x=je=vu0l3g@ljf#d26a73'

SETTINGS_EMAIL_HOST_USER = "dcmdb.email@gmail.com"
SETTINGS_EMAIL_PASS = ""
