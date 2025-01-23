from django.db import models
from student.models import Student


PAYMENT_METHOD_CHOICES = (
    ("Pix", "Pix"),
    ("Dinheiro", "Dinheiro"),
)
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="payment_student")
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)
    discount = models.IntegerField(blank=True, null=True, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student__name']

    def __str__(self):
        return str(self.student)
    
from django.db import models

class PendingPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - Sem pagamentos"