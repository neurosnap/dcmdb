from django.db import models
from django.contrib.auth.models import User

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