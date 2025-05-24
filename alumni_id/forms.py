from django import forms
from .models import IDBackground, AlumniProfile

class IDBackgroundForm(forms.ModelForm):
    class Meta:
        model = IDBackground
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = [
            'school_id', 'first_name', 'last_name', 'year_graduated',
            'company', 'validity_start', 'validity_end', 'contact_number',
            'email', 'photo', 'id_background'
        ]
        widgets = {
            'school_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_graduated': forms.NumberInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'validity_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'validity_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'id_background': forms.Select(attrs={'class': 'form-control'})
        } 