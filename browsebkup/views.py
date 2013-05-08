from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
#uses django's admin User model and default setup
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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
	
	
	return render_to_response('default.html')
	

