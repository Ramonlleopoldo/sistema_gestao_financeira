from django.urls import path
from . import views


urlpatterns = [
    path('training/list/', views.TrainingListView.as_view(), name='training_list'),
    path('training/create/', views.TrainingCreateView.as_view(), name='training_create'),
    path('training/<int:pk>/detail/', views.TrainingDetailsView.as_view(), name='training_detail'),
    path('training/<int:pk>/update/', views.TrainingUpdateView.as_view(), name='training_update'),
    path('training/<int:pk>/delete/', views.TrainingDeleteView.as_view(), name='training_delete'),

    path('location/training/list/', views.LocationTrainingListView.as_view(), name='location_training_list'),
    path('location/training/create/', views.LocationTrainingCreateView.as_view(), name='location_training_create'),
    path('location/training/<int:pk>/update', views.LocationTrainingUpdateView.as_view(), name='location_training_update'),
    path('location/training/<int:pk>/detail', views.LocationTrainingDetailsView.as_view(), name='location_training_detail'),
    path('location/training/<int:pk>/delete', views.LocationTrainingDeleteView.as_view(), name='location_training_delete'),
]
