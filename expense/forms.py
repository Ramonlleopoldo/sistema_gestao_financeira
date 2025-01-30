from django import forms
from . import models


class ExpenseModelForm(forms.ModelForm):
    class Meta:
        model = models.Expense
        fields = ['name', 'value', 'description']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-height: 50px;'}),
            
        }
        labels = {
            'name': 'Nome',
            'value': 'Valor',
            'description': 'Descrição'
        }
    
