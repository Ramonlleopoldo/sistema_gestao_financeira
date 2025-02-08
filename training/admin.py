from django.contrib import admin
from . import models

# Register your models here.
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('location', 'day', 'time',)
    search_fields = ('location', 'day', 'time')

admin.site.register(models.TrainingClass, TrainingAdmin)