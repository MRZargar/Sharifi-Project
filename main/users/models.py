from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    phone_number = models.PositiveIntegerField(null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    UsersTypes = (
        ('is_user', 'user'),
        ('is_operator', 'operator'),
        ('is_admin', 'admin'),
    )

    userType = models.CharField(max_length= 20, choices = UsersTypes, default='is_user')

