from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
@ensure_csrf_cookie
def portal(request):

	context = {}
	dicom_list = [] 
	for path, dirs, files in os.walk(BASE_DIR + '/upload/dicoms/eric/'):
		for d in dirs:
			dicom_list.append(d + '/001.dcm')

	context['dicom_list'] = dicom_list

	return render_to_response('browse_portal.html', context, context_instance = RequestContext(request))
