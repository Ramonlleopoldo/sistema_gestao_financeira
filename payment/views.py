from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from . import models
from student.models import Student
from . import forms
import datetime


class PaymentsPending(ListView):
    model = models.PaymentPending
    template_name = 'payments_pending_list.html'
    context_object_name = 'payments_pending'
    paginate_by = 2

    
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(student__name__icontains=name)

        return queryset


class PaymentPendingDetails(DetailView):
    model = models.PaymentPending
    template_name = 'payment_pending_details.html'
    context_object_name = 'payment'


class PaymentReceivedListView(ListView):
    model = models.PaymentReceived
    template_name = 'payment_received.html'
    context_object_name = 'payments_received'
    paginate_by = 10

    # Recuperando o contexto de ano para usar no input de filtro de ano
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        first_year = 2025
        today_year = datetime.date.today()
        today_year = today_year.year
        if first_year:
            year_list = list(range(first_year, today_year + 1))
        else:
            year_list = []

        context['years'] =  year_list

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        # Filtro pelo nome do aluno
        if name:
            queryset = queryset.filter(student__name__icontains=name)
        
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

class PaymentReceivedDetailView(DetailView):
    model = models.PaymentReceived
    template_name = 'payment_received_detail.html'
    context_object_name = 'pendingpayment'
   



class PaymentCreateView(CreateView):
    model = models.PaymentReceived
    form_class = forms.PaymentModelForm
    template_name = 'payment_create.html'
    success_url = reverse_lazy('payment_pending_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, id=student_id)
        context['student'] = student
        return context

    # Sobrescrevendo o método form_valid para associar o pagamento ao estudante
    def form_valid(self, form):
        form.instance.student = get_object_or_404(Student, id=self.kwargs['student_id'])
        return super().form_valid(form)

