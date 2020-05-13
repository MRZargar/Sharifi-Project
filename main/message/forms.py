from django import forms
from .models import Message

class SendMessageAdmin(forms.ModelForm):


	class Meta:
		model = Message
		fields = ['title', 'reciver_user', 'send_content']



class SendMessageUsers(forms.ModelForm):


	class Meta:
		model = Message
		fields = ['title', 'send_content']