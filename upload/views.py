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
import string
import re
import dicom

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_DIR = BASE_DIR + "/media"

def upload(request):

	if request.method == 'POST':

		error = ""

		temp_file = request.FILES['dicom_file']

		dcm = dicom.read_file(temp_file)

		if temp_file.content_type == "image/dicom" or temp_file.content_type == "image/x-dicom" or temp_file.content_type == "application/dicom":

			#Make media directory if not created already
			if not os.path.exists(MEDIA_DIR):
				os.makedirs(MEDIA_DIR)

			#Users directory of DICOMS
			pre_dir = MEDIA_DIR + '/' + request.user.username

			#Figure out if the record is new or existing
			new_study = request.POST['new_study']

			if new_study == "true":

				new_study = True
				title = request.POST['new_title']

				access = request.POST['status']

				if access == "public":
					public = True
				else:
					public = False

			else:

				new_study = False
				title = request.POST['existing_title']
				study = Study.objects.get(pk = title)

				#Study Instance UID must match for each series within a study
				if study.UID == dcm.StudyInstanceUID:
					pass
				else:
					existing_studies = Study.objects.filter(user_ID = request.user)

					context = { 
						"success": False, 
						"error": "Study Instance UID does not match '" + study.title + "' Study Instance UID", 
						"existing_studies": existing_studies 
					}

					return render_to_response('upload.html', context, context_instance = RequestContext(request))

				title = study.title

				public = study.public

			#driven into madness, all that remains is a whisper
			filename = re.sub(r'[^ \w]+', '', title).replace(" ", "_") + "_" + id_generator()

			# create username folder
			if not os.path.exists(pre_dir):

				os.makedirs(pre_dir)
				os.makedirs(pre_dir + '/public')
				os.makedirs(pre_dir + '/private')

			if public:
				dcm_dir = pre_dir + '/public'
			else:
				dcm_dir = pre_dir + '/private'

			#now upload the file
			my_dicom = processdicom(dicom = dcm)
			dcm = my_dicom.writeFiles(dcm_dir, filename)

			#Test to see if the pixel array is compressed
			if dcm['success'] == False:

				existing_studies = Study.objects.filter(user_ID = request.user)

				context = { 
					"success": False, 
					"error": dcm['error'], 
					"existing_studies": existing_studies 
				}

				return render_to_response('upload.html', context, context_instance = RequestContext(request))

			dcm = dcm['dicom']

			args = {
				"dcm": dcm,
				"dcm_dir": dcm_dir,
				"filename": filename,
				"title": title,
				"public": public,
				"request": request,
				"new_study": new_study
			}

			record = add_dcm_record(**args)

			if record.id:
				success = True
			else:
				success = False
				error = record.error

		elif temp_file.content_type == "application/zip" or temp_file.content_type == "application/octet-stream":

			error = "found zip file, maybe rar"
			success = False

		else:

			error = temp_file.content_type + " is invalid"
			success = False

		existing_studies = Study.objects.filter(user_ID = request.user)

		context = { "success": success, "error": error, "existing_studies": existing_studies }

		return render_to_response('upload.html', context, context_instance = RequestContext(request))

	else:
	
		if request.user.is_authenticated():

			existing_studies = Study.objects.filter(user_ID = request.user)

			context = { "existing_studies": existing_studies }

			return render_to_response('upload.html', context, context_instance = RequestContext(request))
		else:
			return redirect('/users/login')


def handle_uploaded_file(file, dir):
	
    with open(dir, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

#Creates a new record in our database for the DICOM file
#Right now we hard-coded a list of keys we are interested in
def add_dcm_record(**kwargs):

	#dcm, dcm_dir, filename, title, public, request, study

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

	dcm = kwargs['dcm']
	
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
			series_date = convert_date(series_date, "-").encode('utf-8')
		elif tag == "ImageType":
			image_type = dcm.ImageType

	if series_date == "":
		series_date = "1990-01-01"

	# Check for study instance uid
	if kwargs['new_study']:

		try:
			#study = Study.objects.get(UID = study_instance_uid)
			study = Study.objects.get(title = kwargs['title'], user_ID = kwargs['request'].user)

		except (Study.DoesNotExist):

			study = Study.objects.create(
				UID = study_instance_uid,
				user_ID = kwargs['request'].user,
				study_id = study_id,
				study_date = study_date,
				title = kwargs['title'], 
				public = kwargs['public'],
				directory = kwargs['dcm_dir'],
				description = study_description,
				modality = modality,
				institution_name = institution_name,
				manufacturer = manufacturer,
				physician_name = physician_name
			)

			study.save()

	else:

		study = Study.objects.get(title = kwargs['title'], user_ID = kwargs['request'].user)

	try:
		Series.objects.get(UID = series_instance_uid, instance_number = instance_number)
	except (Series.DoesNotExist):

		record = Series.objects.create(
			dcm_study = study,
			UID = series_instance_uid,
			series_number = series_number,
			filename = kwargs['filename'],
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

	record = lambda: None
	record.id = False
	record.error = "Instance number already exists for this study "

	return record

# Method that takes a date "20130513" and converts it to "2013-05-13" or whatever
# delimiter inputed
def convert_date(date, delim):

	year = date[:4]
	month = date[4:6]
	day = date[6:8]

	return delim.join([year, month, day])	

def id_generator(size = 6, chars = string.ascii_lowercase + string.digits):

	return ''.join(random.choice(chars) for x in range(size))
