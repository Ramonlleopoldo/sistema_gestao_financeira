from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Student, PendingPayment

@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, **kwargs):
    """
    Signal para executar ações após salvar um pagamento.
    """
    # Obtém todos os alunos sem pagamentos
    students_without_payments = Student.objects.exclude(
        id__in=Payment.objects.values('student_id')
    )

    # Limpa registros antigos
    PendingPayment.objects.all().delete()

    # Cria novos registros para alunos sem pagamentos
    for student in students_without_payments:
        PendingPayment.objects.create(student=student)
