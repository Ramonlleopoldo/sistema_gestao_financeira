from django import forms
from . import models


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'class_days': forms.Select(attrs={'class': 'form-control'}),
            'class_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'class_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-height: 50px;'}),
        }
        labels = {
            'name': 'Nome',
            'gender': 'Gênero',
            'class_days': 'Dias de aula',
            'class_quantity': "Quantidade de aulas",
            'class_price': 'Valor aula',
            'phone_number': 'Telefone',
            'level': 'Categoria',
            'due_date': 'Vencimento',
            'notes': 'Observações',
        }
        
