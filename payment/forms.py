from django import forms
from . import models


# Form responsavel por confirmar pagamentos e criar registros em pagamentos recebidos
class PaymentModelForm(forms.ModelForm):
    class Meta:
        model = models.PaymentReceived
        fields = ['payment_method', 'amount_paid']

        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 100px;'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'})

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


# Forms responsavel por criar novos pagamentos extras em pagamentos recebidos
class PayExtraModelForm(forms.ModelForm):
     class Meta:
        model = models.PaymentReceived
        fields = ['student', 'payment_method', 'amount_paid']

        widgets = {
            'student':forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 100px;'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'})

        }
        labels = {
            'student': 'Aluno',
            'payment_method': 'Método de pagamento',
            'discount': 'Desconto',
            'amount_paid': 'Valor pago'
        }


# Form Resposanvel por fazer update em pagamentos atrasados
class PaymentUpdate(forms.ModelForm):
    class Meta:
        model = models.PaymentDelay
        fields = ['value_delay']
    
        widgets = {
                'value_delay': forms.NumberInput(attrs={'class': 'form-control'})

            }
        labels = {
                'value_delay': 'Valor atrasado'
        }


# Form responsavel por criar novos pendecias de pagamento em pagamentos atrasados
class PaymentDelayModelForm(forms.ModelForm):
    class Meta:
        model = models.PaymentDelay
        fields = ['student', 'date', 'value_delay']

        widgets = {
            'student':forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'value_delay': forms.NumberInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'student': 'Aluno',
            'date': 'Data referencia',
            'value_delay': 'Valor em atraso',
        }
