from django.contrib import admin
from .models import Setup, Deactivate, Image


admin.site.register(Setup)
admin.site.register(Image)
admin.site.register(Deactivate)