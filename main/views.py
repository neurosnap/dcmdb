from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from upload.models import Study, Series, Image
# JSON encode/decode
import json
from django.db.models import Count

# Create your views here.
def index(request):

	dcms = Series.objects.filter(dcm_study__public = True).select_related

	context = {
		"dcms": dcms
	}
	
	return render_to_response('index.html', context, context_instance = RequestContext(request))

def under_construction(request):

	context = {}
	
	return render_to_response('uc_index.html', context, context_instance = RequestContext(request))

def about(request):

	context = {
		"template": "template.html"
	}
	
	return render_to_response('about.html', context, context_instance = RequestContext(request))

def about_construction(request):

	context = {
		"template": "under_construction.html"
	}

	return render_to_response('about.html', context, context_instance = RequestContext(request))
