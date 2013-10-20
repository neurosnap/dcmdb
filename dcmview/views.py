from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
#you bastard!
import dicom
from dcmupload.models import Study, Series
import json
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_DIR = BASE_DIR + "/media"

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

# Create your views here.
@ensure_csrf_cookie
def view(request, dcm_uid):

	try:

		first_series = Series.objects.get(sop_instance_uid = dcm_uid)

		study = first_series.dcm_study

		series = Series.objects.filter(UID = first_series.UID).order_by("sop_instance_uid")

	except ObjectDoesNotExist:

		context = {
			"success": False,
			"msg": "Object does not exist: " + dcm_uid
		}

		return render_to_response('view.html', context, context_instance = RequestContext(request))

	filepath = MEDIA_DIR + '/' + first_series.filename + '.dcm'

	dcm = dicom.read_file(filepath)

	dcm_dict = getdict(dcm)

	context = {
		"success": True,
		"study": serializers.serialize("json", [study]),
		"series": serializers.serialize("json", series),
		"first_series": serializers.serialize("json", [first_series]),
		"fs": first_series,
		"ss": study,
		"dcm": dcm_dict
	}

	return render_to_response('view.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def study(request, dcm_uid):

	try:

		study = Study.objects.get(UID = dcm_uid)

	except ObjectDoesNotExist:

		context = {
			"success": False,
			"msg": "Object does not exist: " + dcm_uid
		}

		return render_to_response('study.html', context, context_instance = RequestContext(request))

	series = Series.objects.filter(dcm_study = study).distinct("UID")

	context = {
		"success": True,
		"study": study,
		"series": series
	}

	return render_to_response('study.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def series(request, dcm_uid):

	try:

		series = Series.objects.filter(UID = dcm_uid)

	except ObjectDoesNotExist:

		context = {
			"success": False,
			"msg": "Object does not exist: " + dcm_uid
		}

		return render_to_response('series.html', context, context_instance = RequestContext(request))

	context = {
		"success": True,
		"series": series
	}

	return render_to_response('series.html', context, context_instance = RequestContext(request))


def getdict(dcm):

	mydict = {}

	dont_print = ['Pixel Data', 'File Meta Information']

	for key in dcm:
		
		if key.VR == "SQ":

			pass

		else:

			if key.name in dont_print:
				print "item not printed"
			else:
				repr_value = repr(key.value)
				mydict[key.name] = repr_value

	for key in mydict.keys():

		if type(key) is not str:

			try:
				mydict[str(key)] = mydict[key]
			except:
				try:
					mydict[repr(key)] == mydict[key]
				except:
					del mydict[key]

	return json.dumps(mydict, ensure_ascii=False)