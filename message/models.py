from django.db import models
from users.models import CustomUser
from django.template.defaultfilters import slugify
from hashlib import sha256
import datetime
from django.urls import reverse
from random import randrange


class Message(models.Model):
	sender = models.ForeignKey(CustomUser, related_name="+", on_delete=models.CASCADE)
	UsersTypes = (('is_user', 'user'),('is_operator', 'operator'),)
	reciver_user = models.CharField(max_length = 20, choices = UsersTypes, default="is_admin")
	reciver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=60, blank=False)
	date_message = models.DateTimeField(auto_now_add=True)
	send_content = models.TextField(blank=False)
	visualized = models.BooleanField(default=False)
	slug = models.SlugField(null=False, unique=True)
	messageType = models.CharField(max_length=10, default="send")


	def __str__(self):
		return 'Message from ' + self.sender.username + ' and title is ' +self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			random_number = randrange(100, 1000)
			sender_username = self.sender.username 
			time_hash = int(sha256(str(datetime.datetime.now()).encode('utf-8')).hexdigest(), 16 % 10**16)
			slug = str(random_number) + 'U' + sender_username + str(time_hash)[:10]
			self.slug = slugify(slug)
		return super().save(*args, **kwargs)

	def get_absolute_url_send(self):
		return reverse('send_detail', kwargs={'slug': self.slug})

	def get_absolute_url_inbox(self):
		return reverse('inbox_detail', kwargs={'slug': self.slug})


class ResponseMeesage(models.Model):
	message = models.ForeignKey(Message, on_delete=models.CASCADE)
	content = models.TextField(blank=True)
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return 'replay for' + self.message.title + 'author is ' + self.author.username