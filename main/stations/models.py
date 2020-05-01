from django.db import models
from django.contrib.auth import get_user_model
import  os
from django.urls import reverse

def station_directory_path(instance, filename):
	base_name = os.path.basename(filename)
	name,ext = os.path.splitext(base_name)
	return "images/stations/" + str(instance.setup.station_name)+ "/" + str(instance.setup.id) + "/"+"IMG_" + str(instance.setup.id)+ext


class Setup(models.Model):
	operator_name = models.CharField(max_length=150)
	station_name = models.CharField(max_length=150, unique=True)
	address = models.CharField(max_length=255, blank=False)
	description = models.TextField(blank=False)
	date = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=False)


	def __str__(self):
		return self.station_name

	def get_absolute_url(self):
		return reverse('station_detail', args=[str(self.id)])


class Image(models.Model):
	setup = models.ForeignKey(Setup, on_delete=models.CASCADE)
	images = models.ImageField(upload_to=station_directory_path, null=True, blank=True)


	def __str__(self):
		return self.setup.station_name + "Img"


class Deactivate(models.Model):
	operator_name = models.ForeignKey(
				  get_user_model(),
				  on_delete=models.CASCADE,
				  )
	station_name = models.ForeignKey(Setup,
				 	on_delete=models.CASCADE,
				 	related_name='deactivates',
				 	)
	description=models.TextField(blank=False)
	date = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.station_name