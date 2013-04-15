from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
# JSON encode/decode
import json

# Create your views here.
def portal(request):

	context = {}
	
	return render_to_response('portal.html', context, context_instance = RequestContext(request))

def login(request):

	context = {}
	
	return render_to_response('login.html', context, context_instance = RequestContext(request))

def register(request):

	context = {}
	
	return render_to_response('register.html', context, context_instance = RequestContext(request))