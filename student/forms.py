from django import forms
from . import models
from student.models import CLASS_DAYS_CHOICES


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = ['name', 'gender','discount', 'class_price', 'phone_number', 'level', 'due_date', 'status', 'notes']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'class_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
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
            'discount': 'Desconto',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se o objeto já existe e tem valores para 'class_days'
        if self.instance and self.instance.pk:
            # Convertendo os valores salvos (string) de volta para uma lista
            class_days = self.instance.class_days.split(',')
            self.fields['class_days'].initial = class_days

    # Tratamento de name
    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            self.add_error('name', "Este campo é obrigatório.")
            return name

        name = name.strip()

        if not all(c.isalpha() or c.isspace() or c in "-'" for c in name):
            self.add_error('name', "Erro de digitação. Esse campo aceita apenas letras.")
            return name

        return name.title()
    # Tratamento de phone number
    def clean_phone_number(self):
        number = self.cleaned_data.get('phone_number')
        if number:
            number = ''.join(filter(str.isdigit, number))

            if len(number) != 11:
                self.add_error('phone_number', "Número inválido. O número deve ter 11 dígitos.")

        return number
    # tratamento de discount
    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount < 0 or discount > 100:
            self.add_error("discount","Valor de desconto deve ser de 0 a 100")
        return discount
    
    # Tratando due date (vencimento)
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < 1 or due_date > 30:
            self.add_error('due_date', 'Data de vencimento invalida informe uma data de 01 ate 30')
        return due_date
    
    def clean_class_price(self):
        class_price = self.cleaned_data.get('class_price')
        if class_price < 0:
            self.add_error('class_price', 'O valor da aula nao pode ser menor que zero')
        return class_price
    
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
    