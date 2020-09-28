from django import forms
from .models import Setup,Deactivate

class StationSetup(forms.ModelForm):

	class Meta:
		model =  Setup
		fields = ['city', 'address', 'sensor_type', 'latitude', 'longitude', 'owner']



class StationSetup2(forms.ModelForm):

	class Meta:
		model =  Setup
		fields = ['city', 'station_id', 'raspberryID', 'address', 'sensor_type', 'latitude', 'longitude', 'owner',]
		widgets = {'raspberryID': forms.Select()}

	def __init__(self, *args, **kwargs):
		new_choices = kwargs.pop('new_choices')
		super().__init__(*args, **kwargs)
		self.fields['raspberryID'] = forms.ChoiceField(choices=new_choices)
		self.fields['latitude'].widget.attrs['placeholder'] = " number must be six decimal places '0.123456'"
		self.fields['longitude'].widget.attrs['placeholder'] = " number must be six decimal places '0.123456' " 
		self.fields['station_id'].widget.attrs['placeholder'] = " for example abcd1234 " 




class SetupFullForm(forms.ModelForm):
	images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

	class Meta(StationSetup.Meta):
		fields =  StationSetup.Meta.fields + ['images', ]



class StationDeactivate(forms.ModelForm):

	class Meta:
		model = Deactivate
		fields = ['description']