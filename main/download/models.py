from django.db import models
from users.models import CustomUser


class DownloadLink(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	download_link = models.CharField(max_length=5000)
	size = models.PositiveIntegerField(null=True)


	def __str__(self):
		number_of_len_link = len(self.download_link)
		this_size = int(number_of_len_link/2)
		return self.user.username + '_link_' + self.download_link[:this_size] 

