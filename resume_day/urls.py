from django.urls import path
from .views import training_day, dismiss_training, restore_training

urlpatterns = [
    path("training-day/", training_day, name="training_day"),
    path("dismiss-training/<int:training_id>/", dismiss_training, name="dismiss_training"),
    path("restore-training/<int:training_id>/", restore_training, name="restore_training"),
]
