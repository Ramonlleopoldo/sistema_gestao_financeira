from django import forms
from django.core.exceptions import ValidationError
from . import models

class TrainingModelForm(forms.ModelForm):
    class Meta:
        model = models.TrainingClass
        fields = ['student', 'time', 'day', 'location']

        widgets = {
            'student': forms.SelectMultiple(attrs={'class': 'form-select',}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'student': 'Alunos',
            'time': 'Horário',
            'day': 'Dia',
            'location': 'Local'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        time = cleaned_data.get('time')
        day = cleaned_data.get('day')

        if day and time:
            if models.TrainingClass.objects.filter(day=day, time=time).exists():
                raise ValidationError("Já existe um treino para este dia e hora")
        
        return cleaned_data

class LocationModelForm(forms.ModelForm):
    class Meta:
        model = models.LocationTraining
        fields = ['name',]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',}),
        }

        labels = {
            'name': 'Nome',
        }
