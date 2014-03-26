from django.db import models
from django.contrib.auth.models import User

class Study(models.Model):

	UID = models.CharField(max_length = 250, unique = True)
	#user_ID = models.ForeignKey(User)
	study_id = models.CharField(max_length = 250, null = True, blank = True)
	#
	study_date = models.CharField(max_length = 250, null = True, blank = True)
	study_time = models.CharField(max_length = 250, null = True, blank = True)
	#
	accession_number = models.CharField(max_length = 250, null = True, blank = True)
	description = models.CharField(max_length = 2500, null = True, blank = True)
	sop_class_uid = models.CharField(max_length = 250)
	#
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Study._meta.fields]

	def __unicode__(self):
		return self.UID


class Series(models.Model):

	dcm_study = models.ForeignKey(Study)
	UID = models.CharField(max_length = 250)
	series_description = models.TextField(null = True, blank = True)
	modality = models.CharField(max_length = 250, null = True, blank = True)
	institution_name = models.CharField(max_length = 250, null = True, blank = True)
	manufacturer = models.CharField(max_length = 250, null = True, blank = True)
	series_number = models.IntegerField(default = 0, null = True, blank = True)
	#
	body_part_examined = models.CharField(max_length = 250, null = True, blank = True)
	laterality = models.CharField(max_length = 250, null = True, blank = True)
	#
	date = models.CharField(max_length = 250, null = True, blank = True)
	#
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.UID


class Image(models.Model):

	dcm_series = models.ForeignKey(Series)
	UID = models.CharField(max_length = 250)
	filename = models.CharField(max_length = 250)
	image_gen = models.BooleanField(default = False)
	transfer_syntax_uid = models.CharField(max_length = 250, null = True, blank = True)
	#
	image_number = models.IntegerField(default = 0, null = True, blank = True)
	image_orientation_patient = models.CharField(max_length = 250, null = True, blank = True)
	image_position_patient = models.CharField(max_length = 250, null = True, blank = True)
	patient_position = models.CharField(max_length = 250, null = True, blank = True)
	#
	content_date = models.CharField(max_length = 250, null = True, blank = True)
	content_time = models.CharField(max_length = 250, null = True, blank = True)
	#
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.UID