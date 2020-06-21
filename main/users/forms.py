from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number','userType')



class CustomUserCreationForm3(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number','userType')
        widgets = {'userType': forms.Select()}

    def __init__(self, *args, **kwargs):
        new_choices = kwargs.pop('new_choices')
        super().__init__(*args, **kwargs)
        self.fields['userType'].choices = new_choices



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', )



class CustomUserCreationForm2(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number',)
