from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DICOMS(models.Model):
	title = models.CharField(max_length = 50)
	user_ID = models.ForeignKey(User)
	public = models.BooleanField()
	directory = models.CharField(max_length = 500)
	filename = models.CharField(max_length = 500)
	#
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	#
	modality = models.CharField(max_length = 50)
	institution_name = models.CharField(max_length = 50)
	manufacturer = models.CharField(max_length = 50)
	physician_name = models.CharField(max_length = 50)
	#
	bits_allocated = models.IntegerField()
	bits_stored = models.IntegerField()
	study_id = models.CharField(max_length = 50)
	study_date = models.CharField(max_length = 50)
	study_time = models.CharField(max_length = 50)
	study_instance_uid = models.CharField(max_length = 50)
	sop_instance_uid = models.CharField(max_length = 50)
	sop_class_uid = models.CharField(max_length = 50)
	instance_number = models.CharField(max_length = 50)
	accession_number = models.CharField(max_length = 50)
	series_number = models.CharField(max_length = 50)
	#
	image_type = models.CharField(max_length = 50)




