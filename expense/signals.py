from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from .models import Expense, Installment


@receiver(post_save, sender=Expense)
def create_installments(sender, instance, created, **kwargs):
    """
    Este signal é ativado após um Expense ser salvo.
    Ele gera automaticamente as parcelas (Installment) ao criar uma nova despesa.
    """
    if created and instance.installment_count > 1:
        # Calcula o valor de cada parcela
        installment_value = instance.value / instance.installment_count

        # Gera as parcelas com base na quantidade escolhida
        for i in range(instance.installment_count):
            due_date = instance.created_at + relativedelta(months=i)  # Adiciona meses corretamente
            Installment.objects.create(
                expense=instance,
                installment_number=i + 1,
                due_date=due_date,
                installment_value=installment_value
            )
