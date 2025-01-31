from django import forms
from . import models


class PaymentModelForm(forms.ModelForm):
    class Meta:
        model = models.PaymentReceived
        fields = ['payment_method', 'amount_paid']
        
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control', 'style':'max-width: 100px;'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_paid':forms.NumberInput(attrs={'class': 'form-control'})
            
        }
        labels = {
            'payment_method': 'Método de pagamento',
            'discount': 'Desconto',
            'amount_paid': 'Valor pago'
        }

    def clean_amount_paid(self):
        amount_paid = self.cleaned_data.get('amount_paid')
        if amount_paid < 0:
            self.add_error('amount_paid', 'O valor recebido nao pode ser menor que zero')
        return amount_paid
    
