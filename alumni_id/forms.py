from django import forms
from .models import IDBackground, AlumniProfile, Program, College

class IDBackgroundForm(forms.ModelForm):
    class Meta:
        model = IDBackground
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class AlumniProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize college display to show code
        self.fields['college'].queryset = College.objects.all()
        self.fields['college'].label_from_instance = lambda obj: f"{obj.name} ({obj.code})"
        
        # Customize program choices to include college code
        programs = Program.objects.select_related('college').all()
        self.fields['program'].queryset = programs
        self.fields['program'].label_from_instance = lambda obj: f"{obj.name} ({obj.college.code})"
        
        # Create a custom Select widget for programs
        program_choices = [(p.id, f"{p.name} ({p.college.code})") for p in programs]
        program_choices.insert(0, ('', '---------'))
        
        self.fields['program'].widget = forms.Select(
            attrs={
                'class': 'form-select',
                'data-college-field': 'true'
            },
            choices=program_choices
        )
        
        # Add data attributes for college IDs to program options
        for program in programs:
            self.fields['program'].widget.attrs[f'data-college-{program.id}'] = program.college.id

    class Meta:
        model = AlumniProfile
        fields = [
            'school_id', 'first_name', 'last_name', 'college', 'program', 'year_graduated',
            'company', 'validity_start', 'validity_end', 'contact_number',
            'email', 'photo', 'id_background'
        ]
        widgets = {
            'school_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.Select(attrs={
                'class': 'form-select',
                'data-college-select': 'true'
            }),
            'year_graduated': forms.NumberInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'validity_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'validity_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'id_background': forms.Select(attrs={'class': 'form-control'})
        } 