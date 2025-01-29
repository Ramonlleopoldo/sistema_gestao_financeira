from django.db import models
from decimal import Decimal


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
class Student(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    class_days = models.TextField()
    class_quantity = models.IntegerField(blank=True, null= True, default=0)
    class_price = models. DecimalField(max_digits=10, decimal_places=2)
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
        """Retorna o valor total sem desconto."""
        return self.class_price * self.class_quantity

    @property
    def value_discount(self):
        """Retorna o valor total com desconto aplicado."""
        discount = self.discount / Decimal(100)
        value_discount = self.value_total * discount
        return self.value_total - value_discount
    
    def register_payment(self):
        self.status_payment = 'pago'
        self.save()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    