from django.urls import path
from . import views


urlpatterns = [
    path('payments/received/', views.PaymentReceivedListView.as_view(), name='payment_received'),
    path('payments/received/<int:pk>/', views.PaymentReceivedDetailView.as_view(), name='payment_received_detail'),

    path('payments/pending/<int:pk>/', views.PaymentPendingDetails.as_view(), name='payment_pending_detail'),
    path('payments/pending/list/', views.PaymentsPending.as_view(), name='payment_pending_list'),
    
    path('payments/delay/list/', views.PaymentsDelayListView.as_view(), name='payment_delay_list'),
    path('payments/delay/details/<int:pk>', views.PayentDelayDetailsView.as_view(), name='payment_delay_details'),


    path('payments/create/<int:student_id>/', views.PaymentCreateView.as_view(), name='payment_create'),
]
