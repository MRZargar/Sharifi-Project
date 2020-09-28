from django.db import models
from users.models import CustomUser


class DownloadLink(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	stations_id = models.CharField(max_length=2500)
	from_date = models.CharField(max_length=20)
	to_date = models.CharField(max_length=20)
	start_hour = models.PositiveIntegerField()
	end_hour = models.PositiveIntegerField()
	download_link = models.CharField(max_length=5000, blank=True)
	size = models.PositiveIntegerField(blank=True, null=True)
	status = models.BooleanField(default=False)
	request_date = models.DateTimeField(auto_now_add=True)
	number = models.CharField(max_length=500, unique=True)
	dic_delete = models.BooleanField(default=False) 


	def __str__(self):
		return self.user.username + self.status + self.request_date + "stations : " + self.stations_name


