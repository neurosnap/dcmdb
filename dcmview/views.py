from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
#you bastard!
import dicom
from upload.models import Study, Series
import json
import datetime


import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Create your views here.
@ensure_csrf_cookie
def dcmview(request, dcm_id):

	#filepath = BASE_DIR + '/test.dcm'

	study = Study.objects.filter(pk = dcm_id)
	series = Series.objects.filter(dcm_study = study)

	first_series = list(series[:1])[0]

	filepath = BASE_DIR + study[0].directory + '/' + first_series.filename + '.dcm'

	dcm = dicom.read_file(filepath)

	dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

	context = {
		"study": json.dumps(list(study.values()), default=dthandler),
		"series": json.dumps(list(series.values()), default=dthandler),
		"dcm": getdict(dcm)
	}

	return render_to_response('dcmview.html', context, context_instance = RequestContext(request))

def getdict(dcm):

		ddict = {}

		for key in dcm.dir():
			ddict[key] = dcm.get(key) 

		return ddict