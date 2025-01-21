from django.db import models


GENDER_CHOICES = (
    ("F", "Feminino"),
    ("M", "Masculino"),
)
CLASS_DAYS_CHOICES = (
    ("Segunda", "Segunda-feira"),
    ("Terça", "Terça-feira"),
    ("Quarta", "Quarta-feira"),
    ("Quinta", "Quinta-feira"),
    ("Sexta", "sexta-feira"),
    ("Sabado", "Sábado"),
    ("Domingo", "Domingo"),
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
class Student(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    class_days = models.CharField(max_length=20, choices=CLASS_DAYS_CHOICES)
    class_quantity = models.IntegerField()
    class_price = models. DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    due_date = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True, default="Novo")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_att = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    