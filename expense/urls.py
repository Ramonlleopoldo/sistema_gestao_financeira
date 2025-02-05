from django.urls import path
from . import views


urlpatterns = [
    path('expenses/list/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/create/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/<int:pk>/details/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
    path('installment/<int:pk>/', views.InstallmentDetailsview.as_view(), name='installment_detail'),
    path('installment/<int:pk>/pay/', views.MarkInstallmentAsPaidView.as_view(), name='mark_installment_as_paid'),
]
