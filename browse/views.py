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
	loc = BASE_DIR + '/upload/dicoms/'
#	for x in os.walk(loc).next()[1]:
	for dirs in os.walk(loc).next()[1]:
		for subdirs in os.walk(loc + dirs).next()[1]:
			dicom_list.append(dirs + '/' + subdirs)
#			for files in os.walk(loc+dirs+ '/' + subdirs).next()[2]:
#				dicom_list.append(dirs + subdirs + files)
			#dicom_list.append(subdirs)

	context['dicom_list'] = dicom_list

	return render_to_response('browse_portal.html', context, context_instance = RequestContext(request))
@ensure_csrf_cookie
def view(request, params):
	context={}
	fields = params.split('/')
	title = fields[1]
	directory = fields [0]
	context['title'] = title
	context['directory'] = directory
	return render_to_response('view.html', context, context_instance = RequestContext(request))
