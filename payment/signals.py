from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, PaymentReceived
from student.models import Student

@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    # Verifica se o pagamento foi criado e está pendente
    if created and instance.student.status_payment == 'pendente':
        instance.student.register_payment()  # Chama o método para registrar o pagamento
    
    
