from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'phone_number', 'userType', 'is_staff','email_confirmed', 'admin_confirmed', 'active_email_send']
    fieldsets = (
    	(None, {'fields': ('username', 'email', 'phone_number', 'userType', 'password')}),
    	('permissions', {'fields':('is_staff', 'is_active', 'email_confirmed', 'admin_confirmed', 'active_email_send')}),
    	)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'userType','password1', 'password2',
                       'is_staff', 'is_active', 'email_confirmed', 'admin_confirmed', 'active_email_send',
                       )
            }
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)


