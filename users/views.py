from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
#uses django's admin User model and default setup
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
#DICOMS table
from dcmupload.models import Study, Series, Image
#redirects to different page
from django.shortcuts import redirect
#auth default for django
from django.contrib.auth.models import User, Group
#ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
#Force CSRF Cookie
from django.views.decorators.csrf import ensure_csrf_cookie
# email
from django.core.mail import EmailMessage
#mail exception
#from smtplib import SMTPException
# JSON encode/decode
import json
#from django.db.models import Count
from django.conf import settings

domain = settings.DOMAIN

# Create your views here.
@ensure_csrf_cookie
def portal(request):

	#email validation check
	validated = False

	if request.user:
		context = { "user": request.user, "validated": is_email_validated(request.user) }
	
		if request.user.is_authenticated() and request.user.is_active:
			return render_to_response('portal.html', context, context_instance = RequestContext(request))
		else:
			return redirect('/users/login')
	else:
		return redirect('/users/login')

@ensure_csrf_cookie
def login(request):

	context = {}
	
	if request.user.is_authenticated() and request.user.is_active:
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

@ensure_csrf_cookie
def rm(request):

	context = { "user": request.user }
	
	if request.user.is_authenticated():
		return render_to_response('remove.html', context, context_instance = RequestContext(request))
	else:
		return redirect('/users/login')

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
			# redirect('/users')
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

	#send email
	sendValidateEmail(user=req_user, email=req_email)
	
	return HttpResponse('{"success": true, "msg": "Account has been created"}', content_type="application/json")

def validateEmail(request):

	req_email = request.GET['email']

	user = User.objects.get(email__exact=req_email)

	if is_email_validated(user):

		context = { "success": False, "msg": "Account has already been validated" }

	else:

		group = Group.objects.get(name="email_validated")

		group.user_set.add(user)

		group.save()

		context = { "success": True, "msg": "Account has been validated" }

	return render_to_response('validated.html', context, context_instance = RequestContext(request))

def removeUser(request):

	if request.user.is_authenticated:

		user = User.objects.get(email__exact=request.user.email)	

		user.is_active = False

		user.save()

		auth_logout(request)
	
		context = { "success": True, "msg": "Account has been removed" }
	
		return render_to_response('remove.html', context, context_instance = RequestContext(request))

	else:

		redirect('/users/login')

def sendValidation(request):

	sendValidateEmail(user = request.user.username, email = request.user.email)

	return HttpResponse('{"success": true, "msg": "Email validation sent!"}', content_type="application/json")

def sendValidateEmail(**kargs):

	#send email
	email_link = "http://" + domain + "/users/validateEmail?email=" + kargs["email"]
	
	subject = "Welcome to dcmdb!"
	
	body = ("Greetings " + kargs["user"] + "! <br />"
			" Thank you for signing up for dcmdb! <br />"
			" Please click the link below to validate your email address with our website! <br /><br />"
			" <a href='" + email_link + "'>Validate Email</a> ")
	
	to_email = kargs["email"]

	email = EmailMessage(subject, body, to=[to_email])
	email.content_subtype = "html"
	email.send()

def changePass(request):

	if request.user.is_active:
		context = { "active": True, "email": request.user.email }
	else:
		context = { "active": False, "email": "currently anonymous user" }

	print context
	
	return render_to_response('change_pass.html', context, context_instance = RequestContext(request))

def chngPassConfirm(request):

	email = None
	cur_pass = None

	# if an email is present in the POST data then that means they are 
	# requesting a new password without knowing their old password
	if "cur_pass" not in request.POST:
		email = request.POST['email']
	else:
		cur_pass = request.POST['cur_pass']

	new_pass = request.POST['new_pass']

	if email is not None:

		u = User.objects.get(email__exact = email)
		u.set_password(new_pass)
		u.save()

		return HttpResponse('{"success": true, "msg": "Password changed!"}', content_type="application/json")

	else:

		user = authenticate(username = request.user.username, password = cur_pass)

		if user is not None:

			u = User.objects.get(email__exact = request.user.email)
			u.set_password(new_pass)
			u.save()

			return HttpResponse('{"success": true, "msg": "Password changed!"}', content_type="application/json")

		else:

			return HttpResponse('{"success": false, "msg": "Current password is invalid!"}', content_type="application/json")

def sendPass(request):

	user_email = request.POST['user_email']

	try:

		user = User.objects.get(username__exact = user_email)

		#send email
		email_link = "http://" + domain + "/users/reqPass?email=" + user.email
		
		subject = "dcmdb Password Change Request"
		
		body = ("Greetings " + user.username + "! <br />"
				" It appears someone has requested to reset your password. <br />"
				" Please click the link below to finish the password change process with our website! <br /><br />"
				" <a href='" + email_link + "'>Change Password</a> ")
		
		to_email = user.email

		email = EmailMessage(subject, body, to=[to_email])
		email.content_subtype = "html"

		email.send()

		return HttpResponse('{"success": true, "msg": "Password reset sent to email!"}', content_type="application/json")

	except ObjectDoesNotExist:

		try:
			
			user = User.objects.get(email__exact = user_email)

			#send email
			email_link = "http://" + domain + "/users/reqPass?email=" + user.email
			
			subject = "dcmdb Password Change Request"
			
			body = ("Greetings " + user.username + "! <br />"
					" It appears someone has requested to reset your password. <br />"
					" Please click the link below to finish the password change process with our website! <br /><br />"
					" <a href='" + email_link + "'>Change Password</a> ")
			
			to_email = user.email

			email = EmailMessage(subject, body, to=[to_email])
			email.content_subtype = "html"

			email.send()

			return HttpResponse('{"success": true, "msg": "Password reset sent to email!"}', content_type="application/json")

		except ObjectDoesNotExist:

			return HttpResponse('{"success": false, "msg": "Username or email was not found in our records!"}', 
								content_type="application/json")

def reqPass(request):

	context = {
		"req_pass": True,
		"email": request.GET['email']
	}

	return render_to_response('change_pass.html', context, context_instance = RequestContext(request))

def updateInfo(request):

	if request.user and request.user.is_active and request.user.is_authenticated():

		context = {
			"user": request.user
		}

		return render_to_response('update_info.html', context, context_instance = RequestContext(request))

	else:

		return redirect("/users/login")

def saveInfo(request):

	if request.user.is_authenticated():

		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']

		user = User.objects.get(username__exact = request.user.username)

		user.first_name = first_name
		user.last_name = last_name

		user.save()

		return HttpResponse('{"success": true, "msg": "User information has been updated!"}', content_type="application/json")

	else:

		return redirect("users/login")	

def is_email_validated(current_user):

	#A django group, "email_validated" is used to flag whether a user is validated or not
	users_in_group = Group.objects.get(name = "email_validated").user_set.all()

	for user in users_in_group:
		if current_user == user:
			return True

	return False