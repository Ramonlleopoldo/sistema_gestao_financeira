from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from . import models
from student.models import Student
from . import forms


class PaymentsPending(ListView):
    model = models.PaymentPending
    template_name = 'payments_pending_list.html'
    context_object_name = 'payments_pending'

    
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

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        # Filtro pelo nome do aluno
        if name:
            queryset = queryset.filter(student__name__icontains=name)

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


