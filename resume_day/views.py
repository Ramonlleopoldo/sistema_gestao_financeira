from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta
from training.models import TrainingClass, LocationTraining
from . import models


def training_day(request):
    """Exibe os treinos do dia, incluindo os dispensados, e atualiza a quantidade de treinos por local."""
    today = date.today()
    
    # Limpar treinos dispensados do dia anterior
    yesterday = today - timedelta(days=1)
    models.TrainingDismissal.objects.filter(date=yesterday).delete()

    # Mapeamento do dia da semana para português
    dias_semana = {
        "Monday": "seg",
        "Tuesday": "ter",
        "Wednesday": "qua",
        "Thursday": "qui",
        "Friday": "sex",
        "Saturday": "sab",
        "Sunday": "dom"
    }

    # Obtém o dia da semana em inglês e traduz para português
    weekday = today.strftime('%A')  
    translated_day = dias_semana[weekday]  

    # Obtém todos os treinos do dia
    all_trainings = TrainingClass.objects.filter(day=translated_day)

    # Obtém os IDs dos treinos dispensados
    dismissed_trainings = models.TrainingDismissal.objects.filter(date=today).values_list('training', flat=True)

    # Separa os treinos que foram dispensados e os que não foram
    active_trainings = all_trainings.exclude(id__in=dismissed_trainings)
    dismissed_trainings = all_trainings.filter(id__in=dismissed_trainings)

    # Atualiza a contagem de treinos por local, considerando apenas os ativos
    update_location_training_count(active_trainings)

    return render(
        request,
        "training_day.html",
        {
            "active_trainings": active_trainings,  # Treinos ativos
            "dismissed_trainings": dismissed_trainings,  # Treinos dispensados
        }
    )


def update_location_training_count(active_trainings):
    """Atualiza a quantidade de treinos por local, considerando apenas os ativos, sem perder contagens anteriores."""
    # Obtém todos os locais
    locations = LocationTraining.objects.all()

    for location in locations:
        # Conta os treinos ativos para cada local
        active_count = active_trainings.filter(location=location).count()
        
        # Atualiza a quantity_training do local somando os treinos ativos
        location.quantity_training = active_count  # Atualiza a quantidade de treinos para o local
        location.save()
        print(f"Quantidade de treinos para o local {location.name} atualizada para: {location.quantity_training}")  # Depuração


def dismiss_training(request, training_id):
    """Dispensa um treino e redireciona de volta para a página."""
    if request.method == "POST":
        training = get_object_or_404(TrainingClass, id=training_id)
        models.TrainingDismissal.objects.create(training=training, date=date.today())
    
    return redirect("training_day")  # Redireciona para a tela de treinos


def restore_training(request, training_id):
    """Restaura um treino dispensado e redireciona de volta para a página."""
    if request.method == "POST":
        dismissed_training = get_object_or_404(models.TrainingDismissal, training_id=training_id, date=date.today())
        dismissed_training.delete()  # Remove a dispensa do treino
    
    return redirect("training_day")  # Redireciona para a tela de treinos
