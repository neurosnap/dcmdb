from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from dcmupload.models import Study, Series, Image
from django.views.decorators.csrf import ensure_csrf_cookie
# JSON encode/decode
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from itertools import chain

# Create your views here.
@ensure_csrf_cookie
def explore(request):

	image = Image.objects.distinct('dcm_series')

	context = {
		"image": image
	}
	
	return render_to_response('explore.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def search(request):

	query = request.POST['dcm_query']

	context = {
		"hide_search": True,
		"query": query 
	}

	s_study = Study.objects.filter(UID__icontains = query)
	s_series = Series.objects.filter(dcm_study__in = s_study) 
	#s_image = Image.objects.filter(dcm_series__in = s_series).distinct("dcm_series")

	ss_series = Series.objects.filter(UID__icontains = query)
	#ss_image = Image.objects.filter(dcm_series__in = ss_series).distinct("dcm_series")

	#i_image = Image.objects.filter(UID__icontains = query).distinct("dcm_series")

	ii_series = Series.objects.filter(modality__icontains = query)
	#ii_image = Image.objects.filter(dcm_series__in = ii_series).distinct("dcm_series")

	sop_study = Study.objects.filter(sop_class_uid__icontains = query)
	sop_series = Series.objects.filter(dcm_study__in = sop_study)
	#sop_image = Image.objects.filter(dcm_series__in = sop_series).distinct("dcm_series")

	try:
		query.index(":")
		
		q = query.split(":")

		try:
			q_study = Study.objects.filter(**{ q[0]: q[1] })
			q_series = Series.objects.filter(dcm_study__in = q_study)
		except:
			q_series = ""

		try:
			qq_series = Series.objects.filter(**{ q[0]: q[1], q[0]: str(q[1]).capitalize() })
		except:
			qq_series = ""

	except ValueError:

		q_series = ""
		qq_series = ""

	context['image'] = Image.objects.filter( Q(dcm_series__in = s_series) | 
											 Q(dcm_series__in = ss_series) | 
											 Q(UID__icontains = query) | 
											 Q(dcm_series__in = ii_series) | 
											 Q(dcm_series__in = sop_series) | 
											 Q(dcm_series__in = q_series) | 
											 Q(dcm_series__in = qq_series) ).distinct("dcm_series")

	return render_to_response('search.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def index(request):

	context = {}
	
	return render_to_response('index.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def under_construction(request):

	context = {}
	
	return render_to_response('uc_index.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def about(request):

	context = {
		"template": "template.html"
	}
	
	return render_to_response('about.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def dicom(request):

	context = {

	}

	return render_to_response('dicom.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def tos(request):

	context = {

	}

	return render_to_response('tos.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def about_construction(request):

	context = {
		"template": "under_construction.html"
	}

	return render_to_response('about.html', context, context_instance = RequestContext(request))
