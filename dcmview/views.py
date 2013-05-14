from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
import upload.processdicom

# Create your views here.
@ensure_csrf_cookie
def dcmview(request):
	context = {}
	return render_to_response('dcmview.html', context, context_instance = RequestContext(request))
