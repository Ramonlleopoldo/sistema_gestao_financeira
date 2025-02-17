from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from . import models
from student.models import Student
from . import forms
import datetime


class PaymentsPending(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.PaymentPending
    template_name = 'payment_pending/payments_pending_list.html'
    context_object_name = 'payments_pending'
    paginate_by = 10
    permission_required = 'payment.view_paymentpending'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(student__name__icontains=name)

        return queryset


class PaymentPendingDetails(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.PaymentPending
    template_name = 'payment_pending/payment_pending_details.html'
    context_object_name = 'payment'
    permission_required = 'payment.view_paymentpending'


class PaymentReceivedListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.PaymentReceived
    template_name = 'payment_received/payment_received.html'
    context_object_name = 'payments_received'
    paginate_by = 10
    permission_required = 'payment.view_paymentreceived'

    def get_year(self):
        """Verifica a data de criação a partir de 2025 para adicionar nas opções de filtros"""
        first_year = 2025
        today_year = datetime.date.today().year

        return list(range(first_year, today_year + 1))

    # Recuperando o contexto de ano para usar no input de filtro de ano
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = self.get_year()

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


class PaymentReceivedDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.PaymentReceived
    template_name = 'payment_received/payment_received_detail.html'
    context_object_name = 'pendingpayment'
    permission_required = 'payment.view_paymentreceived'


class PaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.PaymentReceived
    form_class = forms.PaymentModelForm
    template_name = 'payment_received/payment_create.html'
    success_url = reverse_lazy('payment_pending_list')
    permission_required = 'payment.add_paymentreceived'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, id=student_id)
        context['student'] = student
        return context

    def form_valid(self, form):
        form.instance.student = get_object_or_404(Student, id=self.kwargs['student_id'])
        form.instance._source_view = "payment_create"  # Definindo a origem
        return super().form_valid(form)


# View resposavel pela criação de pagamento de pagamentos atrasados
class PayDelayCreatedView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.PaymentReceived
    template_name = 'payment_received/payment_delay_created.html'
    form_class = forms.PaymentModelForm
    success_url = reverse_lazy('payment_delay_list')
    permission_required = 'payment.add_paymentreceived'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, id=student_id)
        context['student'] = student

        payment_delay = get_object_or_404(models.PaymentDelay, student=student_id)
        context['payment_delay'] = payment_delay
        return context

    def form_valid(self, form):
        student = get_object_or_404(Student, id=self.kwargs['student_id'])  # Obtendo o estudante
        form.instance.student = student  # Associando o pagamento ao estudante
        form.instance._source_view = "pay_delay_created"  # Definindo a origem
        return super().form_valid(form)


class PayextraCreatedView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.PaymentReceived  # Corrigido de "models" para "model"
    template_name = 'payment_received/pay_extra_created.html'
    form_class = forms.PayExtraModelForm
    success_url = reverse_lazy('payment_pending_list')
    permission_required = 'payment.add_paymentreceived'


class PaymentsDelayListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.PaymentDelay
    template_name = 'payment_delay/payment_delay_list.html'
    context_object_name = 'payments_delay'
    paginate_by = 10
    permission_required = 'payment.view_paymentdelay'


class PaymentDelayCreatedView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.PaymentDelay
    template_name = 'payment_delay/payment_delay_created.html'
    form_class = forms.PaymentDelayModelForm
    success_url = reverse_lazy('payment_delay_list')
    permission_required = 'payment.add_paymentdelay'


class PayentDelayDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.PaymentDelay
    template_name = 'payment_delay/payment_delay_details.html'
    permission_required = 'payment.view_paymentdelay'


class PaymentDelayUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.PaymentDelay
    template_name = 'payment_delay/payment_delay_update.html'
    form_class = forms.PaymentUpdate
    success_url = reverse_lazy('payment_delay_list')
    permission_required = 'payment.change_paymentdelay'


class PaymentDelayDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.PaymentDelay
    template_name = 'payment_delay/payment_delay_delete.html'
    success_url = reverse_lazy('payment_delay_list')
    permission_required = 'payment.delete_paymentdelay'
