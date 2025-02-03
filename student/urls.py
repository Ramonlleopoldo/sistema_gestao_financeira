from django.urls import path
from . import views


urlpatterns = [
    path('student/list/', views.StudentListView.as_view(), name='student_list'),
    path('student/create/', views.StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/detail/', views.StudentDetailView.as_view(), name='student_detail'),
    path('student/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student_update'),
]
