from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
import datetime
from . import models
from . import forms


class ExpenseListView(ListView):
    model = models.Expense
    template_name = 'expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10

    # Recuperando o contexto de ano para usar no input de filtro de ano
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_year = 2025
        today_year = datetime.date.today()
        today_year = today_year.year
        if first_year:
            year_list = list(range(first_year, today_year + 1))
        else:
            year_list = []

        context['years'] = year_list

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


class ExpenseCreateView(CreateView):
    model = models.Expense
    template_name = 'expense_create.html'
    form_class = forms.ExpenseModelForm
    success_url = reverse_lazy('expense_list')


class ExpenseDetailView(DetailView):
    model = models.Expense
    template_name = 'expense_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['installments'] = models.Installment.objects.all()
        return context


class ExpenseDeleteView(DeleteView):
    model = models.Expense
    template_name = 'expense_delete.html'
    success_url = reverse_lazy('expense_list')
