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
import zipfile
import StringIO
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_DIR = BASE_DIR + "/media"

@ensure_csrf_cookie
def zip_dcm(request, uid):

	try:
		dcm = Series.objects.get(sop_instance_uid = uid)
	except ObjectDoesNotExist:
		print "object does not exist: " + uid

	return mk_zip([dcm.filename + '.dcm'], uid)

@ensure_csrf_cookie
def zip_series(request, uid):

	series = Series.objects.filter(UID = uid)

	if not series:
		print "object does not exist: " + uid

	files = []

	for items in series:
		files.append(items.filename + ".dcm")

	return mk_zip(files, uid)

@ensure_csrf_cookie
def zip_study(request, uid):

	try:
		study = Study.objects.get(UID = uid)
		series = Series.objects.filter(dcm_study = study)
	except ObjectDoesNotExist:
		print "object does not exist: " + uid

	files = []

	for items in series:
		files.append(items.filename + ".dcm")

	return mk_zip(files, uid)


def mk_zip(file_list, uid):

	zip_subdir = uid
	zip_filename = "%s.zip" % zip_subdir

	s = StringIO.StringIO()

	zf = zipfile.ZipFile(s, "w")

	for fpath in file_list:

		fdir, fname = os.path.split(fpath)
		zip_path = os.path.join(zip_subdir, fname)

		zf.write(MEDIA_DIR + '/' + fpath, zip_path)

	zf.close()

	resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp