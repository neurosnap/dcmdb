from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
#redirects to different page
from django.shortcuts import redirect
from upload.models import Study, Series, Image
from upload.processdicom import processdicom
# JSON encode/decode
import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import random
import re
import dicom

# new comment :D
# Create your views here.
def upload(request):

	context = {}
	
	if request.user.is_authenticated():
		return render_to_response('upload.html', context, context_instance = RequestContext(request))
	else:
		return redirect('/users/login')

def success(request):

	context = {}

	return render_to_response('success.html', context, context_instance = RequestContext(request))

def upload_dicom(request):

	if request.method == 'POST':

		#Make media directory if not created already
		if not os.path.exists(BASE_DIR + '/media'):
			os.makedirs(BASE_DIR + '/media')

		#Users directory of DICOMS
		pre_dir = BASE_DIR + '/media/' + request.user.username

		#Whether or not the user selected private or public
		access = request.POST['status']

		if access == "public":
			public = True
		else:
			public = False

    	# title data and manipulation
		title = request.POST['title']
		title_rem = re.sub(r'[^ \w]+', '', title)
		title_rem = title_rem.replace(" ", "_")

		filename = title_rem

		# create username folder
		if not os.path.exists(pre_dir):
			os.makedirs(pre_dir)
			os.makedirs(pre_dir + '/public')
			os.makedirs(pre_dir + '/private')

		if public:
			dcm_dir = pre_dir + '/public'
		else:
			dcm_dir = pre_dir + '/private'

		my_dicom = processdicom(request.FILES['dicom_file'])

		# upload file
		dcm = my_dicom.writeFiles(dcm_dir, filename)

		modality = ""
		institution_name = ""
		manufacturer = ""
		physician_name = ""
		bits_allocated = ""
		bits_store = ""
		study_id = ""
		study_description = ""
		study_date = ""
		study_time = ""
		study_instance_uid = ""
		sop_clas_uid = ""
		instance_number = ""
		accession_number = ""
		series_instance_uid = ""
		series_number = ""
		series_date = ""
		image_type = ""
		
		for tag in dcm.dir():

			if tag == "Modality":
				modality = dcm.Modality
			elif tag == "InstitutionName":
				institution_name = dcm.InstitutionName
				institution_name = institution_name.decode('utf-8')
			elif tag == "Manufacturer":
				manufacturer = dcm.Manufacturer
			elif tag == "ReferringPhysicianName":
				physician_name = dcm.ReferringPhysicianName
				physician_name = physician_name.decode('utf-8')
			elif tag == "BitsAllocated":
				bits_allocated = dcm.BitsAllocated
			elif tag == "BitsStored":
				bits_stored = dcm.BitsStored
			elif tag == "StudyID":
				study_id = dcm.StudyID
			elif tag == "StudyDescription":
				study_description = dcm.StudyDescription
				study_description = ""
				# study_description = study_description.decode('utf-8')
			elif tag == "StudyDate":
				study_date = dcm.StudyDate
				study_date = convert_date(study_date, "-")
			elif tag == "StudyTime":
				study_time = dcm.StudyTime
			elif tag == "StudyInstanceUID":
				study_instance_uid = dcm.StudyInstanceUID
			elif tag == "SOPInstanceUID":
				sop_instance_uid = dcm.SOPInstanceUID
			elif tag == "SOPClassUID":
				sop_class_uid = dcm.SOPClassUID
			elif tag == "InstanceNumber":
				instance_number = dcm.InstanceNumber
			elif tag == "AccessionNumber":
				accession_number = dcm.AccessionNumber
			elif tag == "SeriesInstanceUID":
				series_instance_uid = dcm.SeriesInstanceUID
			elif tag == "SeriesNumber":
				series_number = dcm.SeriesNumber
			elif tag == "SeriesDate":
				series_date = dcm.SeriesDate
				series_date = convert_date(series_date, "-")
			elif tag == "ImageType":
				image_type = dcm.ImageType

		# Check for study instance uid
		try:
			study = Study.objects.get(UID = study_instance_uid)
		except (Study.DoesNotExist):

			study = Study.objects.create(
				UID = study_instance_uid,
				user_ID = request.user,
				study_id = study_id,
				study_date = study_date,
				title = title, 
				public = public,
				directory = dcm_dir,
				description = study_description,
				modality = modality,
				institution_name = institution_name,
				manufacturer = manufacturer,
				physician_name = physician_name
			)

			study.save()

		record = Series.objects.create(
			dcm_study = study,
			UID = series_instance_uid,
			filename = filename,
			bits_allocated = bits_allocated,
			bits_stored = bits_stored,
			sop_instance_uid = sop_instance_uid,
			sop_class_uid = sop_class_uid,
			instance_number = instance_number,
			accession_number = accession_number,
			date = series_date
		)

		record.save()

		context = { "record": record.id, "data": dcm.dir() }

		return render_to_response('success.html', context, context_instance = RequestContext(request))

def handle_uploaded_file(f, dcm_dir):
	
    with open(dcm_dir, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Method that takes a date "20130513" and converts it to "2013-05-13" or whatever
# delimiter inputed
def convert_date(date, delim):

	year = date[:4]
	month = date[4:6]
	day = date[6:8]

	return delim.join([year, month, day])	