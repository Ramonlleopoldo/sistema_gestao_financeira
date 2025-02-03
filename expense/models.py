from django.db import models


class Expense(models.Model):
    name = models.TextField(max_length=400)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    installment_count = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Installment(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="prestações")
    installment_number = models.PositiveIntegerField()
    installment_value = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
