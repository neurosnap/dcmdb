dcmdb.org
==========

DCMDB is a DICOM Search Engine and Educational Tool.  

This website was developed by Eric Bower . The mission of this service is to create a repository of easy to access, publicly available, anonymous medical diagnotic images. With this repository we also wish to create a social platform for discussion, teaching, and learning. 

Repository
==========

As a pre-medical student, I found it rather difficult to find a concise location for Digital Imaging and Communications in Medicine (DICOM)  files. There was no way to just search through a maryiad of diagnostic files with some pertinent information about the patient when referencing prognosis, diagnosis, and the rationality behind a diagnosis. I feel as though there is a market for an educational tool to assist in the teaching and learning process of diagnostic imaging and the tools required to make judgements on those images. One of my goals with this project is to create a platform that at its base is a repository to store, retrieve anonymous diagnostic data easily and efficiently. 

Discussion
==========

I am a strong proponent of crowd-sourcing, or the act of collaborating with a multiplicity of voluntarily interested people seeking to accomplish some common goal. Why can we not apply this principle to medicine as well? However, there doesn't seem to be an efficient way to receive feedback from an aggregate of physicians. Typically, in my experience, physicians will send their DICOM files to a specific set of people to receive second opinions. While this is an effective approach for most purposes, I am betting that if crowd-sourcing is done properly, we can create an environment where hundreds or thousands of knowledgable people discuss patient DICOM files. 

Teaching
==========

Once we have created a platform for discussion, we can use that discussion as an educational tool for aspiring physicians or even hobbyists. In my opinion, understanding the rationale and critiqueing of any analysis lends itself to wisdom, reason, and progress. When intelligence criticizes intelligence, we reach a level of understanding that is greater than the sum of its parts, because that wisdom can then be applied to other fields of interest. 

Learning
==========

We need to get people interested in medicine to learn about the reality of that career path earlier in their lives. I think it is a shame that as a pre-medical student in Neuroscience, we barely learned about the actual day-to-day happenings of a career in medicine. Why is it we have to wait until medical school to learn about and how to properly observe diagnostic tools such as DICOMs? 

Contributing
==========

```
Copyright 2013 Nysus Solutions, LLC.

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

Volunteers are welcome to help make the service run more efficiently, effectively.  This project was developed in Python, the Django framework, and Postgresql.  The production server is hosted by Amazon on an Ubuntu EC2 virtualized server.  It uses gunicorn as the WSGI HTTP Server and nginx as the Proxy HTTP Server.

It should be noted that the development environment defaults to sqlite3.

#### HOW TO DEVELOP ON DEBIAN-DIST (UBUNTU)

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

Start working on a virtualevn
```
$ workon dcmdb
```

deactivate virtualenv (just an example, dont do this now)
```
$ deactivate
```

Now install python dependencies
```
$ pip install -r python_dependencies.txt
```

python_dependencies.txt
```
Django==1.5.4
Pillow==2.2.1
South==0.8.2
argparse==1.2.1
matplotlib==1.3.0
nose==1.3.0
numpy==1.7.1
pydicom==0.9.8
pyparsing==2.0.1
python-dateutil==2.1
setproctitle==1.1.8
six==1.4.1
tornado==3.1.1
yolk==0.4.3
```

##### HOW TO INSTALL GDCM

###### PRE-REQS

```
apt-get install cmake-curses-gui
apt-get install libpcre3 libpcre3-dev
```

###### SWIG

  * Download the latest version of SWIG
  * Extract compressed file e.g. swig-2.0.11

```
$ cd swig-2.0.11
$ ./configure
$ make
$ make install
```

###### GDCM

  * Download the latest version of GDCM
  * Extract compressed file e.g. gdcm.tar.bz2

```
$ mkdir gdcm-build
$ cd gdcm
$ rm CMakeCache.txt
$ cd ../gdcm-build
$ ccmake ../gdcm
```

  * Screen will come up,
  * Press [T] to go to advanced mode
  * SET CMAKE\_C\_FLAGS to -fPIC
  * SET CMAKE\_CXX\_FLAGS to -fPIC [Could be optional]
  * Press [C] to configure
  * SET GDCM\_WRAP\_PYTHON to ON
  * [G] to generate

```
$ make
$ make install
```

###### Git

```
$ apt-get install git-core
```

##### Download DCMDB

SSH: git@github.com:neurosnap/dcmdb.git
HTTPS: https://github.com/neurosnap/dcmdb.git

```
$ git clone git@github.com:neurosnap/dcmdb.git
$ cd dcmdb
$ python manage.py syncdb
$ python manage.py migrate
$ python manage.py runserver
```

Then, in browser http://localhost:8000

Done!

#### HOW TO DEVELOP ON WINDOWS (Get ready for hell)

##### Install python 2.7

Add C:/Python27;C:/Python27/Scripts;C:/Python27/Lib;C:/Python27/DLLs; to environmental variables

##### Install cygwin 32 bit -- ALERT! For pydicom to properly install, select "Install for Just Me"

Install the following cygwin packages:

 * wget

Open cygwin
This creates a shortcut to allow us to use Python in interactive mode without specifying -i
```
$ mkshortcut -D -n "Cygwin Console" -i /Cygwin.ico /bin/bash -a --login
```

##### setuptools
```
$ wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
$ python ez_setup.py
```

##### Install PIP + Virtualenv
```
$ easy_install pip
$ easy_install virtualenv
$ easy_install virtualenvwrapper
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

Start working on a virtualevn
```
$ workon dcmdb
```

deactivate virtualenv (just an example, dont do this now)
```
$ deactivate
```

##### Install the rest of the dependencies that actually work through PIP
```
$ pip install -r python\_dependencies\_windows.txt
```

python\_dependencies\_windows.txt
```
Django==1.5.4
South==0.8.2
argparse==1.2.1
nose==1.3.0
pydicom==0.9.8
pyparsing==2.0.1
python-dateutil==2.1
six==1.4.1
tornado==3.1.1
yolk==0.4.3
```

##### Install matplotlib 32 bit v1.3.1+ via installer

  * http://matplotlib.org/downloads.html

##### Install numpy via installer

##### Install pillow via installer

##### Install gdcm v2.4.0+ via installer

  * http://sourceforge.net/projects/gdcm/files/gdcm%202.x/GDCM%202.4.0/

Add C:/Program Files (x86)/GDCM 2.4.0/bin to envrionmental variables

Move C:/Program Files (x86)/GDCM 2.4.0/ to C:/Python27/Lib/site-packages
  * _gdcmswig.pyd
  * gdcm.py
  * gdcmswig.py

##### Install msysgit via installer
Add to environmental variables

##### Download DCMDB
```
$ git clone git@github.com:neurosnap/dcmdb.git
$ cd dcmdb
$ python manage.py syncdb
$ python manage.py migrate
$ python manage.py runserver
```

Then, in browser http://localhost:8000

Done!