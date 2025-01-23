from django import forms
from . import models
from student.models import CLASS_DAYS_CHOICES


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
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
    class_days = forms.MultipleChoiceField(
        choices=CLASS_DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Dias de aula"
    )
    def save(self, commit=True):
        # Obtendo a instância do modelo sem salvar ainda
        instance = super().save(commit=False)
        
        # Convertendo a lista de dias selecionados para string (separados por vírgulas)
        instance.class_days = ','.join(self.cleaned_data['class_days'])

        if instance.phone_number == None:
            instance.phone_number = " "

        # Salvando a instância no banco, se necessário
        if commit:
            instance.save()
        
        return instance
    
