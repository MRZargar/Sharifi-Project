from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    phone_number = models.PositiveIntegerField(null=True, blank=True, unique=True)

    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_operator = models.BooleanField(default=False)
