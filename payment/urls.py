from django.urls import path
from . import views


urlpatterns = [
    path('payments/received/', views.PaymentReceivedListView.as_view(), name='payment_received' ),
    path('payments/received/<int:pk>/', views.PaymentReceivedDetailView.as_view(), name='payment_received_detail'),
    
    path('payments/<int:pk>/', views.PaymentDetails.as_view(), name='payment_detail'),
    path('payments/list/', views.Payments.as_view(), name='payment_list' ),

    path('payments/create/<int:student_id>/', views.PaymentCreateView.as_view(), name='payment_create'),
]