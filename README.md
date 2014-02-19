dcmdb.org
==========

DCMDB is a DICOM Search Engine and Educational Tool.  

This website was developed by Eric Bower . The mission of this service is to create a repository of easy to access, publicly available, anonymous medical diagnotic images. With this repository we also wish to create a social platform for discussion, teaching, and learning. 

Contributing
==========

```
Copyright 2013 Eric Bower

dcmdb is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

dcmdb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with dcmdb.  If not, see <http://www.gnu.org/licenses/>.
```

Volunteers are welcome to help make the service run more efficiently, effectively.  
This project was developed in Python, the Django framework, and Postgresql.  
The production server is hosted by Amazon on an Ubuntu EC2 virtualized server.  
It uses gunicorn as the WSGI HTTP Server and nginx as the Proxy HTTP Server.

INSTALL
=========

Windows 
---------

##### Prereqs

  *  Python 2.7 (determine whether 32 or 64 bit)
  *  Microsoft Visual C++ 2008 Redistributable Package 
  (identical 32 or 64 bit as python) 
  [32 bit](http://www.microsoft.com/en-us/download/details.aspx?displaylang=en&id=29) 
  [64 bit](http://www.microsoft.com/en-us/download/details.aspx?id=15336)
  *  Git

##### Install Postgresql

http://www.postgresql.org/download/windows/

Set password for "postgres" user
Open pgAdmin III
Connect to PostgreSQL
Create database "dcmdb" set owner to "postgres"

##### Download DCMDB

SSH - git@github.com:neurosnap/dcmdb.git

[HTTPS](https://github.com/neurosnap/dcmdb.git)

```
$ git clone git@github.com:neurosnap/dcmdb.git
$ cd dcmdb
```

Download: https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
Install setuptools

##### setuptools
```
$ cd /path/to/ez_setup.py
$ python ez_setup.py install
```

##### Install PIP
```
$ easy_install pip
```

##### Install the rest of the dependencies that actually work through PIP
```
$ pip install -r dependencies.txt
```

dependencies.txt
```
Django==1.5.4
South==0.8.2
psycopg2==2.5.1
argparse==1.2.1
nose==1.3.0
pydicom==0.9.8
pyparsing==2.0.1
python-dateutil==2.1
six==1.4.1
bleach==1.2.2
html5lib==0.95
yolk==0.4.3
```

##### Set up local django settings file

Create dicomdb/settings_dev.py file
```
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

##### Run 

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


HOW TO DEVELOP ON DEBIAN-DIST (UBUNTU)
---------

```
$ apt-get update
$ apt-get upgrade
$ apt-get install python-pip
$ pip install virtualenv
$ mkdir ~/.virtualenvs
$ pip install virtualenvwrapper
$ vim ~/.bash_profile
```

in .bash_profile
```
export WORKON_HOME=~/.virtualenvs
/usr/local/bin/virtualenvwrapper.sh
```

Make a virtualenv
```
$ mkvirtualenv dcmdb
```

Start working on a virtualenv (after mkvirtualenv it usually loads right into the virt)
```
$ workon dcmdb
```

deactivate virtualenv (just an example, dont do this now)
```
$ deactivate
```

Now install python dependencies
```
$ pip install -r ./conf/dependencies.txt
```

dependencies.txt
```
Django==1.5.4
Pillow==2.2.1
South==0.8.2
nose==1.3.0
psycopg2==2.5.1
pydicom==0.9.8
pyparsing==2.0.1
python-dateutil==2.1
setproctitle==1.1.8
six==1.4.1
yolk==0.4.3
```

##### Download DCMDB

SSH - git@github.com:neurosnap/dcmdb.git

[HTTPS](https://github.com/neurosnap/dcmdb.git)

```
$ git clone git@github.com:neurosnap/dcmdb.git
$ cd dcmdb
```

Create dicomdb/settings_dev.py file
```
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

##### Run

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
