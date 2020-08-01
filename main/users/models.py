from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, validators=[MinLengthValidator(10)],null=False, blank=False, unique=True)
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    admin_confirmed = models.BooleanField(default=False)
    active_email_send = models.BooleanField(default=False)
    UsersTypes = (
        ('is_user', 'user'),
        ('is_operator', 'operator'),
        ('is_admin', 'admin'),
    )

    userType = models.CharField(max_length= 20, choices = UsersTypes, default='is_user')

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)
    instance.profile.save()