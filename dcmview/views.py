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

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_DIR = BASE_DIR + "/media"

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

# Create your views here.
@ensure_csrf_cookie
def dcmview(request, dcm_uid):

	try:

		study = Study.objects.filter(UID = dcm_uid)

	except ObjectDoesNotExist:

		print "study does not exist"
	
	series = Series.objects.filter(dcm_study = study)

	first_series = list(series[:1])[0]

	filepath = MEDIA_DIR + '/' + first_series.filename + '.dcm'

	dcm = dicom.read_file(filepath)

	dcm_dict = getdict(dcm)

	context = {
		"study": json.dumps(list(study.values()), default=dthandler),
		"series": json.dumps(list(series.values()), default=dthandler),
		"dcm": dcm_dict
	}

	return render_to_response('dcmview.html', context, context_instance = RequestContext(request))

@ensure_csrf_cookie
def dcmseries(request, series_id):

	series = Series.objects.filter(pk = series_id)
	study = list(series[:1])[0].dcm_study
	#study = Study.objects.filter(pk = list(series[:1])[0].dcm_study.id)

	filepath = BASE_DIR + study.directory + '/' + list(series[:1])[0].filename + '.dcm'
	print filepath

	context = {}

	context['study'] = study
	context['dcm'] = getdict(dicom.read_file(filepath))

	return HttpResponse(json.dumps(context, default=dthandler, ensure_ascii=False), content_type="application/json")
	#return render_to_response('dcmview.html', context, context_instance = RequestContext(request))


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