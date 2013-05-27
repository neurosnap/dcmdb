from django.db import models
from django.contrib.auth.models import User
from django import forms

class Study(models.Model):

	UID = models.CharField(max_length = 100)
	user_ID = models.ForeignKey(User)
	study_id = models.CharField(max_length = 50)
	study_date = models.DateField()
	title = models.CharField(max_length = 50)
	public = models.BooleanField()
	directory = models.CharField(max_length = 100)
	description = models.CharField(max_length = 500)
	#
	modality = models.CharField(max_length = 50)
	institution_name = models.CharField(max_length = 50)
	manufacturer = models.CharField(max_length = 50)
	physician_name = models.CharField(max_length = 50)
	#
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	#

# Create your models here.
class Series(models.Model):

	dcm_study = models.ForeignKey(Study)
	UID = models.CharField(max_length = 100)
	filename = models.CharField(max_length = 100)
	#
	bits_allocated = models.IntegerField()
	bits_stored = models.IntegerField()
	#
	sop_instance_uid = models.CharField(max_length = 100)
	sop_class_uid = models.CharField(max_length = 100)
	#
	instance_number = models.CharField(max_length = 100)
	accession_number = models.CharField(max_length = 100)
	#
	date = models.DateField()
	#
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Image(models.Model):

	UID = models.CharField(max_length = 100)
	series_ID = models.ForeignKey(Series)
	number = models.IntegerField()
	image_position_patient = models.CharField(max_length = 50)
	pixel_offset = models.IntegerField()
	slice_location = models.DecimalField(decimal_places = 5, max_digits = 20)

class UploadFileForm(forms.Form):

	new_or_existing_options = (('new', 'New Series -- Do you want this DICOM to be part of a new collection of DICOM files?'), 
				('existing', 'Existing Series -- Do you want this DICOM to be part of an existing collection of DICOM files?'))

	status_options = (('public', 'Public -- Anyone can view this DICOM file',), 
				('private', 'Private -- Only you or people you should it with can view this DICOM file',))

	new_or_existing = forms.ChoiceField(widget = forms.RadioSelect, choices = new_or_existing_options)

	title = forms.CharField(max_length = 50)
    
	dicom_file  = forms.FileField(widget = forms.FileInput)

	status = forms.ChoiceField(widget = forms.RadioSelect, choices = status_options)