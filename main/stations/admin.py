from django.contrib import admin
from .models import Setup, Deactivate, Image, Access


admin.site.register(Setup)
admin.site.register(Image)
admin.site.register(Deactivate)
admin.site.register(Access)