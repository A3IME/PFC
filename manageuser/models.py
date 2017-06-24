from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
import hashlib

class Directories(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	directory = models.CharField(max_length=32)
	
	REQUIRED_FIELDS = ['directory']

def create_directory(sender, **kwargs):
	user = kwargs["instance"]

	ho = hashlib.sha256(str(user.id).encode())
	if kwargs["created"]:
		user_directory = Directories(user=user, directory=ho.hexdigest())
		user_directory.save()
post_save.connect(create_directory, sender=settings.AUTH_USER_MODEL)
