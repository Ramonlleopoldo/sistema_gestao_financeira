from django.db import models
from decimal import Decimal
from django.db.models import Case, When, Value, IntegerField


GENDER_CHOICES = (
    ("F", "Feminino"),
    ("M", "Masculino"),
)
CLASS_DAYS_CHOICES = (
    ("Seg", "Segunda-feira"),
    ("Ter", "Terça-feira"),
    ("Qua", "Quarta-feira"),
    ("Qui", "Quinta-feira"),
    ("Sex", "sexta-feira"),
    ("Sab", "Sábado"),
    ("Dom", "Domingo"),
)
LEVEL_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("I", "I"),
    ("PRO", "PRO"),
)
STATUS_CHOICES = (
    ("Regular", "Regular"),
    ("Parou", 'Parou'),
    ("Novo", "Novo"),
    ("Retornou", "Retornou")
)
STATUS_PAYMENT_CHOICES = (
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
)
BILLING_METHOD_CHOICES = (
    ('aula', 'Aula'),
    ('mensal', 'Mensal')
)


class Student(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    class_days = models.TextField()
    class_quantity = models.IntegerField(blank=True, null=True, default=0)
    billing_method = models.CharField(max_length=10, choices=BILLING_METHOD_CHOICES)
    class_price = models. DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    discount = models.IntegerField()
    phone_number = models.CharField(max_length=15, blank=True, null=True, default=" ")
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    due_date = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    status_payment = models.CharField(max_length=10, choices=STATUS_PAYMENT_CHOICES, default='pendente')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_att = models.DateTimeField(auto_now=True)

    @property
    def value_total(self):
        if self.billing_method == "aula":
            """Retorna o valor total sem desconto."""
            value = self.class_price * self.class_quantity
        if self.billing_method == "mensal":
            value = self.class_price
        return value

    @property
    def value_discount(self):
        """Retorna o valor total com desconto aplicado."""
        discount = self.discount / Decimal(100)
        value_discount = self.value_total * discount
        return self.value_total - value_discount

    class Meta:
        ordering = [
            Case(
                When(status='Parou', then=Value(4)),
                When(status='Retornou', then=Value(3)),
                When(status='Novo', then=Value(2)),
                When(status='Regular', then=Value(1)),
                default=Value(5),
                output_field=IntegerField()
            ),
        ]

    def __str__(self):
        return self.name
