from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
import datetime
from . import models
from . import forms
from training.models import LocationTraining


class ExpenseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Expense
    template_name = 'expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10
    permission_required = 'expense.view_expense'

    # Recuperando o contexto de ano para usar no input de filtro de ano
    def get_year(self):
        """Verifica a data de criação a partir de 2025 para adicionar a opção de filtros"""

        first_year = 2025
        today_year = datetime.date.today().year

        return list(range(first_year, today_year + 1))

    def get_expenses_with_installments(self, expenses):
        """Adiciona os dados de parcelas à lista de despesas"""
        expenses_with_installments = []
        for expense in expenses:
            installments = expense.installments.all()  # Relacionamento reverso
            installment_pay = installments.filter(status="Pago").count()
            installment_quantity = installments.count()

            expense.installment_pay = installment_pay
            expense.installment_quantity = installment_quantity
            expenses_with_installments.append(expense)

        return expenses_with_installments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # anos a partir de 2025
        context['years'] = self.get_year()

        # Anotações de parcelas
        context['expenses'] = self.get_expenses_with_installments(context['expenses'])

        # Retorna o contexto de quantidade de treinos por arena
        training_brasil = LocationTraining.objects.get(name="Arena Brasil")
        training_criciuma = LocationTraining.objects.get(name="Arena Criciuma")
        context['brasil'] = training_brasil.quantity_training
        print(context['brasil'])
        context['criciuma'] = training_criciuma.quantity_training
        print(context['criciuma'])

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtro pelo nome
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        # Filtro por mês e ano
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')

        if month and year:
            # Filtrando por mês e ano
            queryset = queryset.filter(
                created_at__month=month,
                created_at__year=year
            )
        elif month:
            # Filtrando apenas pelo mês
            queryset = queryset.filter(created_at__month=month)
        elif year:
            # Filtrando apenas pelo ano
            queryset = queryset.filter(created_at__year=year)

        return queryset


class ExpenseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Expense
    template_name = 'expense_create.html'
    form_class = forms.ExpenseModelForm
    success_url = reverse_lazy('expense_list')
    permission_required = 'expense.add_expense'


class ExpenseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Expense
    template_name = 'expense_detail.html'
    permission_required = 'expense.view_expense'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['installments'] = models.Installment.objects.all()
        return context


class InstallmentDetailsview(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Installment
    template_name = 'installment_detail.html'
    permission_required = 'expense.view_installment'


class MarkInstallmentAsPaidView(LoginRequiredMixin, View):
    def post(self, request, pk):
        installment = get_object_or_404(models.Installment, id=pk)
        installment.status = 'Pago'
        # Registra a data de pagamento
        installment.date_payment = datetime.date.today()
        installment.save()
        return redirect('installment_detail', pk=installment.id)


class ExpenseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Expense
    template_name = 'expense_delete.html'
    success_url = reverse_lazy('expense_list')
    permission_required = 'expense.delete_expense'
