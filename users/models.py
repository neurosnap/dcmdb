from django.db import models

# Create your models here.
class Users(models.Model):
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)
	email = models.CharField(max_length = 50)
	password = models.CharField(max_length = 20)
	active = models.BooleanField(default = False)
	validated = models.BooleanField(default = False)
	pub_date = models.DateTimeField('date created')