from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from . import forms


class ExpenseListView(ListView):
    model = models.Expense
    template_name = 'expense_list.html'
    context_object_name = 'expenses'


class ExpenseCreateView(CreateView):
    model = models.Expense
    template_name = 'expense_create.html'
    form_class = forms.ExpenseModelForm
    success_url = reverse_lazy('expense_list')


class ExpenseDetailView(DetailView):
    model = models.Expense
    template_name = 'expense_detail.html'


class ExpenseUpdateView(UpdateView):
    model = models.Expense
    template_name = 'expense_update.html'
    form_class = forms.ExpenseModelForm
    success_url = reverse_lazy('expense_list')

class ExpenseDeleteView(DeleteView):
    model = models.Expense
    template_name = 'expense_delete.html'
    success_url = reverse_lazy('expense_list')