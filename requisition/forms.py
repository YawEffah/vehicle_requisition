from django import forms
from .models import CarRequest, Vehicle

class CarRequestForm(forms.ModelForm):
    class Meta:
        model = CarRequest
        fields = ['purpose', 'description', 'destination', 'vehicle', 'start_datetime', 'return_datetime']
        widgets = {
            'purpose': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Purpose of the car request'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where do you want to go?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Provide description'
            }),
            'vehicle': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_datetime': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'return_datetime': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter available vehicles for the 'vehicle' field
        self.fields['vehicle'].queryset = Vehicle.objects.filter(is_available=True)

    def clean_return_datetime(self):
        start_datetime = self.cleaned_data.get('start_datetime')
        return_datetime = self.cleaned_data.get('return_datetime')
        
        if start_datetime and return_datetime and return_datetime <= start_datetime:
            raise forms.ValidationError('Return datetime must be later than start datetime')
        
        return return_datetime

    


class CreateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'make', 'model', 'year', 'picture']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter license number...'}),
            'make': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter car make...'}),
            'model': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter car model...'}),
            'year': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter manufactured year...'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Upload a picture of the car...'}),
        }

