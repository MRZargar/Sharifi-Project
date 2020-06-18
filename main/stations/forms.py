from django import forms
from .models import Setup,Deactivate


class StationSetup(forms.ModelForm):

	class Meta:
		model =  Setup
		fields = ['station_name', 'address', 'sensor_type', 'latitude', 'longitude', 'description']



class StationSetup2(forms.ModelForm):

	class Meta:
		model =  Setup
		fields = ['station_name', 'raspberryID', 'address', 'sensor_type', 'latitude', 'longitude', 'description',]
		widgets = {'raspberryID': forms.Select()}

	def __init__(self, *args, **kwargs):
		new_choices = kwargs.pop('new_choices')
		super().__init__(*args, **kwargs)
		self.fields['raspberryID'] = forms.ChoiceField(choices=new_choices)



class SetupFullForm(forms.ModelForm):
	images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

	class Meta(StationSetup.Meta):
		fields =  StationSetup.Meta.fields + ['images', ]



class StationDeactivate(forms.ModelForm):

	class Meta:
		model = Deactivate
		fields = ['description']