from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
# JSON encode/decode
import json

# Create your views here.
def index(request):

	context = {}
	
	return render_to_response('index.html', context, context_instance = RequestContext(request))

def about(request):

	context = {}
	
	return render_to_response('about.html', context, context_instance = RequestContext(request))

def under_construction(request):

	context = {}
	
	return render_to_response('under_construction.html', context, context_instance = RequestContext(request))