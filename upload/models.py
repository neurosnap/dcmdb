from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DICOMS(models.Model):
	title = models.CharField(max_length = 50)
	user_ID = models.ForeignKey(User)
	public = models.BooleanField()
	directory = models.CharField(max_length = 100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	modality = models.CharField(max_length = 100)
	institution_name = models.CharField(max_length = 100)


