from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
#redirects to different page
from django.shortcuts import redirect
from upload.models import Study, Series, Image, UploadFileForm
from upload.processdicom import processdicom
# JSON encode/decode
import json
import os
import random
import re
import dicom

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_DIR = BASE_DIR + "/media"

def upload(request):

	if request.method == 'POST':

		form = UploadFileForm(request.POST, request.FILES)

		temp_file = request.FILES['dicom_file']

		error = ""

		if form.is_valid():

			if temp_file.content_type == "image/dicom" or temp_file.content_type == "image/x-dicom" or temp_file.content_type == "application/dicom":

				#Make media directory if not created already
				if not os.path.exists(MEDIA_DIR):
					os.makedirs(MEDIA_DIR)

				#Users directory of DICOMS
				pre_dir = MEDIA_DIR + '/' + request.user.username

				#Whether or not the user selected private or public
				access = request.POST['status']

				if access == "public":
					public = True
				else:
					public = False

		    	# title data and manipulation
				title = request.POST['title']
				filename = re.sub(r'[^ \w]+', '', title).replace(" ", "_")
				#title_rem = title_rem.replace(" ", "_")

				#filename = title_rem

				# create username folder
				if not os.path.exists(pre_dir):
					os.makedirs(pre_dir)
					os.makedirs(pre_dir + '/public')
					os.makedirs(pre_dir + '/private')

				if public:
					dcm_dir = pre_dir + '/public'
				else:
					dcm_dir = pre_dir + '/private'

				my_dicom = processdicom(temp_file)

				# upload file
				dcm = my_dicom.writeFiles(dcm_dir, filename)

				record = add_dcm_record(dcm, dcm_dir, filename, title, public, request)

				if record.id:
					success = True
				else:
					success = False

			elif temp_file.content_type == "application/zip" or temp_file.content_type == "application/octet-stream":

				error = "found zip file, maybe rar"
				success = False

			else:

				error = temp_file.content_type + " is invalid"
				success = False
				
		else:

			error = "Validation didnt pass"
			success = False

		if success:
			form = UploadFileForm()

		context = { "success": success, "error": error, "form": form }

		return render_to_response('upload.html', context, context_instance = RequestContext(request))

	else:

		form = UploadFileForm()

		context = { "form": form }
	
		if request.user.is_authenticated():
			return render_to_response('upload.html', context, context_instance = RequestContext(request))
		else:
			return redirect('/users/login')


def handle_uploaded_file(file, dir):
	
    with open(dir, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

#Creates a new record in our database for the DICOM file
#Right now we hard-coded a list of keys we are interested in
def add_dcm_record(dcm, dcm_dir, filename, title, public, request):

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

	return record

# Method that takes a date "20130513" and converts it to "2013-05-13" or whatever
# delimiter inputed
def convert_date(date, delim):

	year = date[:4]
	month = date[4:6]
	day = date[6:8]

	return delim.join([year, month, day])	