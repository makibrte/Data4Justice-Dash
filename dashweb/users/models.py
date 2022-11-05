
from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
	'''
	Our UserProfile model extends the built-in Django User Model
	'''
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	

	
	has_profile = models.BooleanField(default = False)
	
	is_active = models.BooleanField(default = True)

	def __str__(self):
		return f'{self.user}'

