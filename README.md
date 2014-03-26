dcmdb.org
==========

DCMDB is a DICOM Search Engine and Educational Tool.  

This website was developed by Eric Bower . The mission of this service is to create a repository of easy to access, publicly available, anonymous medical diagnotic images. With this repository we also wish to create a social platform for discussion, teaching, and learning. 

Contributing
==========

Volunteers are welcome to help make the service run more efficiently, effectively.  
This project was developed in Python, the Django framework, and Postgresql.  
The production server is hosted by Amazon on an Ubuntu EC2 virtualized server.  
It uses gunicorn as the WSGI HTTP Server and nginx as the Proxy HTTP Server.

INSTALL
=========

#### HOW TO DEVELOP ON DEBIAN-DIST (UBUNTU)

Install python dependencies
```
$ pip install -r ./conf/dependencies.txt
```

#### Install PostgreSQL

```
$ apt-get install postgresql postgresql-contrib
```

##### Configure PostgreSQL

```
$ sudo su - postgres
$ createdb dcmdb
$ createuser -P
$ psql
postgres=# GRANT ALL PRIVILEGES ON DATABASE dcmdb TO username;
postgres=# \q
$ logout
```

Create dcmdb/settings_env.py file
```
DEBUG = True

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "dcmdb",
    "USER": "postgres",
    "PASSWORD": ""
  }
}

EMAIL_HOST_USER = ''
EMAIL_PASS = ''
```

```
$ python manage.py syncdb
$ python manage.py migrate
$ python manage.py runserver
```

Then, in browser http://localhost:8000

There is one django group that is used as a flag for email validation

If you get an error like "GROUP not found" when going to /users:

  * Go to: http://localhost:8000/admin
  * Login and select "Groups"
  * Add Group "email_validated"
  * Save

Done!