from django.urls import path
from . import views


urlpatterns = [
    path('payments/pending/', views.PaymentPendingListView.as_view(), name='payment_pending' ),
    path('payments/received/', views.PaymentsReceivedListView.as_view(), name='payment_received' ),
    path('payments/create/<int:student_id>/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('payments/received/<int:pk>/', views.PaymentReceivedDetailView.as_view(), name='payment_received_detail'),
    path('payments/pending/<int:pk>/', views.PaymentPendingDetailView.as_view(), name='payment_pending_detail'),
]