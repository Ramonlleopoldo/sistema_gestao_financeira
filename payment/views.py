from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from . import models
from student.models import Student
from . import forms

# pagamentos pendentes
class PaymentPendingListView(ListView):
    model = models.PendingPayment
    template_name = 'payment_pending.html'
    context_object_name = 'payments_pending'

    
class PaymentsReceivedListView(ListView):
    model = models.Payment
    template_name = 'payments_received.html'
    context_object_name = 'payments'
    

class PaymentCreateView(CreateView):
    model = models.Payment
    form_class = forms.PaymentModelForm
    template_name = 'payment_create.html'
    success_url = reverse_lazy('payment_pending')

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


class PaymentReceivedDetailView(DetailView):
    model = models.Payment
    template_name = 'payment_received_detail.html'


class PaymentPendingDetailView(DetailView):
    model = models.PendingPayment
    template_name = 'payment_pending_detail.html'
