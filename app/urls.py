from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path("", include('student.urls')),
    path("", include('payment.urls')),
    path("", include('expense.urls')),
    path("", include('training.urls')),
    path("", include('resume_day.urls')),
]
