from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
#redirects to different page
from django.shortcuts import redirect
from upload.models import DICOMS
#from upload import processdicom
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

		pre_dir = BASE_DIR + '/upload/dicoms/' + request.user.username

		# create username folder
		if not os.path.exists(pre_dir):
			os.makedirs(pre_dir)

    	# title data and manipulation
		title = request.POST['title']
		title_rem = re.sub(r'[^ \w]+', '', title)
		title_rem = title_rem.replace(" ", "_")

		filename = request.POST['fname']

		# create dicom set folder
		#if not os.path.exists(pre_dir + '/' + title_rem):
		#	os.makedirs(pre_dir + '/' + title_rem)

		dcm = dicom.read_file(request.FILES['dicom_file'])
		
		for tag in dcm.dir():

			if tag == "Modality":
				modality = dcm.Modality
			elif tag == "InstitutionName":
				institution_name = dcm.InstitutionName
			elif tag == "Manufacturer":
				manufacturer = dcm.Manufacturer
			elif tag == "ReferringPhysicianName":
				physician_name = dcm.ReferringPhysicianName
			elif tag == "BitsAllocated":
				bits_allocated = dcm.BitsAllocated
			elif tag == "BitsStored":
				bits_stored = dcm.BitsStored
			elif tag == "StudyID":
				study_id = dcm.StudyID
			elif tag == "StudyDate":
				study_date = dcm.StudyDate
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
			elif tag == "SeriesNumber":
				series_number = dcm.SeriesNumber
			elif tag == "ImageType":
				image_type = dcm.ImageType

		access = request.POST['status']

		if access == "public":
			public = True
		else:
			public = False

		record = DICOMS.objects.create(
			title = title_rem, 
			user_ID = request.user,
			public = public,
			directory = pre_dir + '/' + title_rem,
			filename = filename,
			modality = modality,
			institution_name = institution_name,
			manufacturer = manufacturer,
			physician_name = physician_name,
			bits_allocated = bits_allocated,
			bits_stored = bits_stored,
			study_id = study_id,
			study_date = study_date,
			study_time = study_time,
			study_instance_uid = study_instance_uid,
			sop_instance_uid = sop_instance_uid,
			sop_class_uid = sop_class_uid,
			instance_number = instance_number,
			accession_number = accession_number,
			series_number = series_number,
			image_type = image_type)

		record.save()

		#dcm_dir = pre_dir + '/' + title_rem + '/'
		#dicom_dir = pre_dir + '/' + title_rem + '/'

		#my_dicom = processdicom.processdicom(request.FILES['dicom_file'])

		#my_dicom.writeFiles(dicom_dir, title_rem)
		# upload file
		#handle_uploaded_file(request.FILES['dicom_file'], dcm_dir + '.dcm')

		# grab DICOM data
		# dcm = dicom.read_file(dcm_dir + '.dcm')

		# img = pylab.imshow(dcm.pixel_array, cmap = pylab.cm.bone)
		# img.savefig(dcm_dir + '.png', dpi=300)

		context = { "record": record.id, "data": dcm.dir() }

		return render_to_response('success.html', context, context_instance = RequestContext(request))

def handle_uploaded_file(f, dcm_dir):
	
    with open(dcm_dir, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

