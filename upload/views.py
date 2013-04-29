from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
#redirects to different page
from django.shortcuts import redirect
# JSON encode/decode
import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import random
import dicom
import re

# Create your views here.
def upload(request):

	context = {}
	
	if request.user.is_authenticated():
		return render_to_response('upload.html', context, context_instance = RequestContext(request))
	else:
		return redirect('/users/login')

def success(request):

	context = {}

	return render_to_response('success.html', context, context_instance = RequestContext(request))

def upload_dicom(request):

	if request.method == 'POST':

		pre_dir = BASE_DIR + '/upload/dicoms/' + request.user.username

		# create username folder
		if not os.path.exists(pre_dir):
			os.makedirs(pre_dir)

    	# title data and manipulation
		title = request.POST['title']
		title_rem = re.sub(r'[^ \w]+', '', title)
		title_rem = title_rem.replace(" ", "_")

		# create dicom set folder
		if not os.path.exists(pre_dir + '/' + title_rem):
			os.makedirs(pre_dir + '/' + title_rem)

		dcm_dir = pre_dir + '/' + title_rem + '/001.dcm'
		
		# upload file
		handle_uploaded_file(request.FILES['dicom_file'], dcm_dir)

		# grab DICOM data
		dcm = dicom.read_file(dcm_dir)

		context = { "patient": dcm, "patient_keys": dcm.dir() }

		return render_to_response('success.html', context, context_instance = RequestContext(request))

def handle_uploaded_file(f, dcm_dir):
	
    with open(dcm_dir, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

