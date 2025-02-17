from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models
from payment.models import PaymentPending, PaymentReceived, PaymentDelay
import calendar
import datetime


@receiver(post_save, sender=models.Student)
def day_class(sender, instance, created, **kwargs):

    """verifica a quantidade de dias que tem na semana para calcular o campo de quantidade de treinos que o aluno terá"""

    # Desconectar temporariamente o signal para evitar loop infinito
    post_save.disconnect(day_class, sender=models.Student)

    date = datetime.date.today()

    semanas = calendar.monthcalendar(date.year, date.month)

    seg, ter, qua, qui, sex, sab, dom = 0, 0, 0, 0, 0, 0, 0
    for semana in semanas:
        if semana[0] != 0:
            seg += 1
        if semana[1] != 0:
            ter += 1
        if semana[2] != 0:
            qua += 1
        if semana[3] != 0:
            qui += 1
        if semana[4] != 0:
            sex += 1
        if semana[5] != 0:
            sab += 1
        if semana[6] != 0:
            dom += 1
    dias_treino = instance.class_days
    soma = 0
    if 'Seg' in dias_treino:
        soma += seg
    if 'Ter' in dias_treino:
        soma += ter
    if 'Qua' in dias_treino:
        soma += qua
    if 'Qui' in dias_treino:
        soma += qui
    if 'Sex' in dias_treino:
        soma += sex
    if 'Sab' in dias_treino:
        soma += sab
    if 'Dom' in dias_treino:
        soma += dom
    instance.class_quantity = soma
    instance.save()
    # Reconectando signals após salvar
    post_save.connect(day_class, sender=models.Student)


# Após salvar ou att um aluno o signals verifica se o status do pagamento é pendente se for ele cria um registro no models payment-pending
@receiver(post_save, sender=models.Student)
def att_payment_pending(sender, instance, created, **kwargs):

    if instance.status_payment == "pendente":
        PaymentPending.objects.get_or_create(
            student=instance,
        )


"""Após ser confirmado o pagamento de um aluno ele exclui o aluno de payment_pending e cria um registro no payment_received além disso muda o status_payment para 'pago' dessa forma o aluno nao é adicionado novamente em payment_pending
"""

"""Realizamos um verificação para idenficar de qual url esta vindo o pagamento, se for de pagamento_atrasado apenas removemos da lista de pagamento atrasados se for de paymanet_cretaed removemos da lista de pagamento pendentes e atualizamos o vaor de status_payment para pago"""

@receiver(post_save, sender=PaymentReceived)
def remove_payment_pending(sender, instance, **kwargs):
    if hasattr(instance, "_source_view"):
        if instance._source_view == "pay_delay_created":
            print("Pagamento atrasado confirmado")
            PaymentDelay.objects.filter(student=instance.student).delete()
            instance.student.save()
            pass
        elif instance._source_view == "payment_create":
            print("Pagamento do mês atual confirmado")
            PaymentPending.objects.filter(student=instance.student).delete()
            instance.student.status_payment = "pago"
            instance.student.save()
