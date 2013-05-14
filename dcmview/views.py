from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
import upload.processdicom
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
@ensure_csrf_cookie
def dcmview(request):
	filepath = BASE_DIR + '/test.dcm'
	context = {} 
	context['dcm'] = upload.processdicom.processdicom(filepath).getdict()
	return render_to_response('dcmview.html', context, context_instance = RequestContext(request))
