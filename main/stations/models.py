from django.db import models
from django.contrib.auth import get_user_model
import  os
from django.urls import reverse
from users.models import CustomUser
import datetime
def station_directory_path(instance, filename):
	base_name = os.path.basename(filename)
	name,ext = os.path.splitext(base_name)
	return "images/stations/" + str(instance.setup.station_name)+ "/" + str(instance.setup.id) + "/"+"IMG_" + str(instance.setup.id)+ext


class Setup(models.Model):
	operator = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
	table_name = models.CharField(max_length=50, null=True)
	station_name = models.CharField(max_length=150, unique=True)
	address = models.CharField(max_length=300, blank=False)
	description = models.TextField(blank=True, null=True)
	date = models.DateTimeField(default=datetime.datetime.now())
	status = models.BooleanField(default=False)
	sensorTypes = (('type1', 'TYPE1'), ('type2', 'TYPE2'),)
	sensor_type = models.CharField(max_length=50, choices = sensorTypes, default='type1')
	latitude = models.DecimalField(max_digits=20, decimal_places=10, blank=False)
	longitude = models.DecimalField(max_digits=20, decimal_places=10, blank=False)
	health = models.IntegerField(default=0)
	raspberryID = models.IntegerField(blank=False, null=False)
	health_time = models.DateTimeField(default=datetime.datetime.now())

	def __str__(self):
		return self.station_name

	def get_absolute_url(self):
		return reverse('station_detail', args=[str(self.id)])


class Image(models.Model):
	setup = models.ForeignKey(Setup, on_delete=models.CASCADE)
	images = models.ImageField(upload_to=station_directory_path, null=False, blank=False)


	def __str__(self):
		return self.setup.station_name + "Img"


class Deactivate(models.Model):
	operator = models.ForeignKey(CustomUser, on_delete=models.PROTECT)


	station_name = models.ForeignKey(Setup,
				 	on_delete=models.CASCADE,
				 	related_name='deactivates',
				 	)
	description=models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return str(self.station_name) if self.station_name else ""


class Access(models.Model):
	station = models.ForeignKey(Setup, on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


	def __str__(self):
		return self.station.station_name + "_Access"


class Raspberry(models.Model):
	raspberryID = models.IntegerField(unique=True, blank=False, null=False)

	def __str__(self):
		return str(self.raspberryID)
