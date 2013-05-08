from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
@ensure_csrf_cookie
def portal(request):

	context = {}

	return render_to_response('browse_portal.html', context, context_instance = RequestContext(request))
