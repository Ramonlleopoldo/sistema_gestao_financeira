from django.db import models
from student.models import Student


class LocationTraining(models.Model):
    name = models.CharField(max_length=200)
    quantity_training = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TrainingClass(models.Model):
    DAYS_CHOICES = (
        ('seg', 'Segunda-Feira'),
        ('ter', 'Terça-Feira'),
        ('qua', 'Quarta-Feira'),
        ('qui', 'Quinta-Feira'),
        ('sex', 'Sexta-Feira'),
        ('sab', 'Sabádo'),
        ('dom', 'Domingo'),
    )
    student = models.ManyToManyField(Student, related_name='training_classes')
    location = models.ForeignKey(LocationTraining, on_delete=models.PROTECT, related_name='location_training')
    time = models.TimeField()
    day = models.CharField(max_length=40, choices=DAYS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day', 'time']

    def __str__(self):
        return f"{self.get_day_display()} - {self.time} ({self.location})"
