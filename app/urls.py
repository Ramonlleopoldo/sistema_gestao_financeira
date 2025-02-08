from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path("", include('student.urls')),
    path("", include('payment.urls')),
    path("", include('expense.urls')),
    path("", include('training.urls')),
]
