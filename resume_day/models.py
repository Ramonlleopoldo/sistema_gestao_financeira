from django.db import models
from training.models import TrainingClass


class TrainingDismissal(models.Model):
    training = models.ForeignKey(TrainingClass, on_delete=models.CASCADE)
    date = models.DateField()  # Data em que o treino foi dispensado
    reason = models.TextField(blank=True, null=True)  # Motivo da dispensa (opcional)

    def __str__(self):
        return f"Treino {self.training} dispensado em {self.date}"
