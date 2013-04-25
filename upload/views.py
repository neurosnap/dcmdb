from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
# JSON encode/decode
import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import random

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

	context = { "form": form }

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)

		if form.is_valid():
			handle_uploaded_file(request.FILES['file'], request.user)
			return redirect('/upload/success')
	else:
		form = UploadFileForm()

	return render_to_response('upload.html', context, context_instance = RequestContext(request))

def handle_uploaded_file(f, user):
	
    with open(BASE_DIR + '/upload/dicoms/' + user.username + '_' + str(random.randrange(10, 1000000)) + '.dicom', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

