from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
from payment import models

@receiver(post_save, sender=Student)
def payment_post_save(sender, instance, **kwargs):
    """
    Signal para executar ações após salvar um novo aluno.
    ação de atualizar o modelo de pagamentos pendentes (PendingPayment)
    """
    # Obtém todos os alunos sem pagamentos
    students_without_payments = Student.objects.exclude(
        id__in=models.Payment.objects.values('student_id')
    )

    # Limpa registros antigos
    models.PendingPayment.objects.all().delete()

    # Cria novos registros para alunos sem pagamentos
    for student in students_without_payments:
        models.PendingPayment.objects.create(student=student)
