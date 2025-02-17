from django.db import models
from student.models import Student


PAYMENT_METHOD_CHOICES = (
    ("Pix", "Pix"),
    ("Dinheiro", "Dinheiro"),
)


class PaymentPending(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="payment_pending_student")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.student)


class PaymentReceived(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_received_student')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name


class PaymentDelay(models.Model):
    MONTH_CHOICES = [
        ('01', 'Janeiro'),
        ('02', 'Fevereiro'),
        ('03', 'Março'),
        ('04', 'Abril'),
        ('05', 'Maio'),
        ('06', 'Junho'),
        ('07', 'Julho'),
        ('08', 'Agosto'),
        ('09', 'Setembro'),
        ('10', 'Outubro'),
        ('11', 'Novembro'),
        ('12', 'Dezembro'),
    ]
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='payment_delay_student')
    date = models.CharField(max_length=2, choices=MONTH_CHOICES)
    value_delay = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
