# student/management/commands/create_pending_payments.py
from django.core.management.base import BaseCommand
from student.models import Student
from payment.models import PaymentPending

class Command(BaseCommand):
    help = "Cria pagamentos pendentes para estudantes com status_payment = 'pendente'."

    def handle(self, *args, **kwargs):
        # Filtra estudantes com status_payment = 'pendente'
        pending_students = Student.objects.filter(status_payment="pendente")
        
        # Cria os pagamentos pendentes
        payments = [
            PaymentPending(student=student)
            for student in pending_students
        ]
        
        # Salva os pagamentos pendentes no banco de dados usando bulk_create
        PaymentPending.objects.bulk_create(payments)
        
        # Mensagem de sucesso
        self.stdout.write(self.style.SUCCESS(f"{len(payments)} pagamentos pendentes criados com sucesso."))