# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from upload.models import Study, Series, Image, UploadFileForm
from upload.processdicom import processdicom
# JSON encode/decode
import json
import random
import string
import re
import dicom
import os
#ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
#Force CSRF Cookie
from django.views.decorators.csrf import ensure_csrf_cookie

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_DIR = BASE_DIR + "/media"

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

@ensure_csrf_cookie
def dcmupload(request):

	context = {}

	return render_to_response('dcmupload.html', context, context_instance = RequestContext(request))

def handle_uploaded_file(file, dir):
	
    with open(dir, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

# Method that takes a date "20130513" and converts it to "2013-05-13" or whatever
# delimiter inputed
def convert_date(date, delim):

	year = date[:4]
	month = date[4:6]
	day = date[6:8]

	return delim.join([year, month, day])	

def id_generator(size = 6, chars = string.ascii_lowercase + string.digits):

	return ''.join(random.choice(chars) for x in range(size))