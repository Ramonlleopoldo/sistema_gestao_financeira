from django.urls import path
from . import views


urlpatterns = [
    path('payments/received/', views.PaymentReceivedListView.as_view(), name='payment_received'),
    path('payments/received/<int:pk>/', views.PaymentReceivedDetailView.as_view(), name='payment_received_detail'),

    path('payments/pending/<int:pk>/', views.PaymentPendingDetails.as_view(), name='payment_pending_detail'),
    path('payments/pending/list/', views.PaymentsPending.as_view(), name='payment_pending_list'),
    
    path('payments/delay/list/', views.PaymentsDelayListView.as_view(), name='payment_delay_list'),
    path('payments/delay/created/', views.PaymentDelayCreatedView.as_view(), name='payment_delay_created'),
    path('payments/delay/<int:pk>/update/', views.PaymentDelayUpdateView.as_view(), name='payment_delay_update'),
    path('payments/delay/details/<int:pk>', views.PayentDelayDetailsView.as_view(), name='payment_delay_details'),
    path('payments/delay/delete/<int:pk>', views.PaymentDelayDeleteView.as_view(), name='payment_delay_delete'),


    path('payments/create/<int:student_id>/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('pay/delay/create/<int:student_id>/', views.PayDelayCreatedView.as_view(), name='pay_delay_created'),
    path('pay/extra/create/', views.PayextraCreatedView.as_view(), name='pay_extra_created')
]
