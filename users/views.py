from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
#uses django's admin User model and default setup
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
#DICOMS table
from upload.models import DICOMS
#redirects to different page
from django.shortcuts import redirect
#auth default for django
from django.contrib.auth.models import User, Group
#ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
#Force CSRF Cookie
from django.views.decorators.csrf import ensure_csrf_cookie
# email
from django.core.mail import send_mail
#mail exception
#from smtplib import SMTPException
# JSON encode/decode
import json

# Create your views here.
@ensure_csrf_cookie
def portal(request):

	#email validation check
	validated = False

	#A django group, "email_validated" is used to flag whether a user is validated or not
	users_in_group = Group.objects.get(name = "email_validated").user_set.all()
	for user in users_in_group:
		if request.user == user:
			validated = True

	# public and private DICOMS
	public_dcms = DICOMS.objects.filter(user_ID = request.user, public = True)
	private_dcms = DICOMS.objects.filter(user_ID = request.user, public = False)

	context = { "user": request.user, "validated": validated, "public": public_dcms, "private": private_dcms }
	
	if request.user.is_authenticated():
		return render_to_response('portal.html', context, context_instance = RequestContext(request))
	else:
		return redirect('/users/login')

@ensure_csrf_cookie
def login(request):

	context = {}
	
	if request.user.is_authenticated():
		return redirect('/users/')
	else:	
		return render_to_response('login.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def logout(request):

	auth_logout(request)
	
	return redirect('/')

@ensure_csrf_cookie
def register(request):

	context = {}
	
	return render_to_response('register.html', context, context_instance = RequestContext(request))

def checkUniqueUser(request):

	req_user = request.POST['user']

	try:
		# Try to find user
		u = User.objects.get(username__exact=req_user)
		return HttpResponse('{"success": false, "msg": "User already exists"}', content_type="application/json")
	except ObjectDoesNotExist:
		# No user found!
		return HttpResponse('{"success": true, "msg": "User is available"}', content_type="application/json")

def checkUniqueEmail(request):

	req_email = request.POST['email']

	try:
		u = User.objects.get(email__exact=req_email)
		return HttpResponse('{"success": false, "msg": "Email already exists"}', content_type="application/json")
	except ObjectDoesNotExist:
		return HttpResponse('{"success": true, "msg": "Email is available"}', content_type="application/json")

def checkLogin(request):

	req_user = request.POST['user']
	req_pass = request.POST['pass']

	user = authenticate(username = req_user, password = req_pass)

	if user is not None:
		if user.is_active:
			auth_login(request, user)
			# Redirect to a success page.
			return HttpResponse('{"success": true, "msg": "Login Successful"}', content_type="application/json")
		else:
			# Account is disabled
			return HttpResponse('{"success": false, "msg": "Account is disabled"}', content_type="application/json")
	else:
		# Invalid Login
		return HttpResponse('{"success": false, "msg": "Invalid Login"}', content_type="application/json")

def createUser(request):

	req_user = request.POST['user']
	req_email = request.POST['email']
	req_pass = request.POST['pass']

	u = User.objects.create_user(req_user, req_email, req_pass)
	u.save()

	#send email(
	sendValidateEmail({ "user": req_user, "email": req_email })
	
	return HttpResponse('{"success": true, "msg": "Account has been created"}', content_type="application/json")

def validateEmail(request):

	req_email = request.GET['email']

	user = User.objects.get(email__exact=req_email)

	group = Group.objects.get(name="email_validated")

	group.user_set.add(user)

	group.save()

	context = { "success": True, "msg": "Account has been validated" }

	return render_to_response('validated.html', context, context_instance = RequestContext(request))

def removeUser(request):

	request.user.is_active = False

	request.user.save()

	auth_logout(request)
	
	context = { "success": True, "msg": "Account has been removed" }
	
	return render_to_response('removed.html', context, context_instance = RequestContext(request))

def sendValidateEmail(**kargs):

	#send email
	email_link = "http://127.0.0.1/users/validateEmail?email=" + kargs["email"]
	subject = "Welcome to DICOMDB!"
	body = ("Greetings " + kargs["user"] + "! <br />"
			" Thank you for signing up for DICOM DB! <br />"
			" Please click the link below to validate your email address with our website! <br /><br />"
			" <a href='" + email_link + "'>Validate Email</a> ")
	from_email = "webmaster@dicomdb.org"
	to_email = kargs["email"]

	send_mail(subject, body, from_email, [to_email], fail_silently=False)