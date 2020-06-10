from django import forms
from .models import Setup,Deactivate


class StationSetup(forms.ModelForm):

	class Meta:
		model =  Setup
		fields = ['station_name', 'address', 'latitude', 'longitude', 'description']


class SetupFullForm(forms.ModelForm):
	images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

	class Meta(StationSetup.Meta):
		fields =  StationSetup.Meta.fields + ['images', ]



class StationDeactivate(forms.ModelForm):

	class Meta:
		model = Deactivate
		fields = ['description']