from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
# JSON encode/decode
import json

# Create your views here.
def portal(request):

	context = {}
	
	if request.user.is_authenticated():
		return render_to_response('portal.html', context, context_instance = RequestContext(request))
	else:
		return redirect('/users/login')

def login(request):

	context = {}
	
	if request.user.is_authenticated():
		return redirect('/users/')
	else:	
		return render_to_response('login.html', context, context_instance = RequestContext(request))

def logout(request):

	auth_logout(request)
	
	return redirect('/')

def register(request):

	context = {}
	
	return render_to_response('register.html', context, context_instance = RequestContext(request))

def checkLogin(request):

	req_user = request.POST['user']
	req_pass = request.POST['pass']

	user = authenticate(username = req_user, password = req_pass)

	if user is not None:
		if user.is_active:
			auth_login(request, user)
			# Redirect to a success page.
			return HttpResponse('{"success": true, "msg": "Login Successful!"}', content_type="application/json")
		else:
			# Account is disabled
			return HttpResponse('{"success": false, "msg": "Account is disabled"}', content_type="application/json")
	else:
		# Invalid Login
		return HttpResponse('{"success": false, "msg": "Invalid Login"}', content_type="application/json")

