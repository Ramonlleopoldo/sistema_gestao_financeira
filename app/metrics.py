from payment.models import PaymentReceived
from payment.models import PaymentPending
from django.utils.formats import number_format
from student.models import Student
from expense.models import Expense, Installment
from payment.models import PaymentDelay
import datetime


# Buscando métricas de pagamentos, total recebido, total de estudante que ja pagaram, valor total a receber e quantidade de alunos que nao pagaram
def get_sales_metric():
    date = datetime.date.today()
    payment_received = PaymentReceived.objects.all()
    payment_pending = PaymentPending.objects.all()
    # Total Recebido
    total_received = sum(payment.amount_paid for payment in payment_received)

    # Número de estudantes que ja pagaram
    total_student_received = sum(1 for payment in payment_received if payment.created_at.month == date.month and payment.created_at.year == date.year)

    # Total de dinheiro pendente (Á receber)
    total_payment_pending = sum(payment.student.value_discount for payment in payment_pending)

    # Número de estudantes que faltam pagar
    payment_student_pending = sum(1 for payment in payment_pending if payment.created_at.month == date.month)

    # Total de dinheiro atraso
    payment_delay = PaymentDelay.objects.all()
    total_payment_delay = sum(payment.value_delay for payment in payment_delay)

    # Total de Alunos com pagamento atrasado
    total_student_payment_delay = payment_delay.count()

    # calculo despesas do mês
    expenses = Expense.objects.all()
    installments = Installment.objects.all()
    expense_month_in_cash = sum(expense.value for expense in expenses if expense.installment_count == 1)
    expense_month_in_installment = 0
    expense_future = 0
    for expense in expenses:
        if expense.installment_count > 1:
            for installment in installments:
                # Calculo de despesas do mês
                if installment.expense.id == expense.id and installment.status == "Pago":
                    if date.month == installment.date_payment.month:
                        expense_month_in_installment += installment.installment_value
                # Calculo despesas futuras
                elif installment.expense.id == expense.id and installment.status == "Pendente":
                    expense_future += installment.installment_value
    expense_month = expense_month_in_cash + expense_month_in_installment

    return dict(
        total_received=number_format(total_received, decimal_pos=2, force_grouping=True),
        total_student_received=total_student_received,
        total_payment_pending=number_format(total_payment_pending, decimal_pos=2, force_grouping=True),
        payment_student_pending=payment_student_pending,
        expense_month_value=number_format(expense_month, decimal_pos=2, force_grouping=True),
        expense_future_value=number_format(expense_future, decimal_pos=2, force_grouping=True),
    )


# Buscando estudantes por categoria e gênero
def get_students_metric():
    students = Student.objects.all()

    # Buscando estudantes por categoria e gênero
    total_student_fa = sum(1 for student in students if student.level == "A" and student.gender == "F" and student.status != "Parou")
    total_student_ma = sum(1 for student in students if student.level == "A" and student.gender == "M" and student.status != "Parou")
    total_student_fb = sum(1 for student in students if student.level == "B" and student.gender == "F" and student.status != "Parou")
    total_student_mb = sum(1 for student in students if student.level == "B" and student.gender == "M" and student.status != "Parou")
    total_student_fc = sum(1 for student in students if student.level == "C" and student.gender == "F" and student.status != "Parou")
    total_student_mc = sum(1 for student in students if student.level == "C" and student.gender == "M" and student.status != "Parou")
    total_student_fd = sum(1 for student in students if student.level == "D" and student.gender == "F" and student.status != "Parou")
    total_student_md = sum(1 for student in students if student.level == "D" and student.gender == "M" and student.status != "Parou")
    total_student_fi = sum(1 for student in students if student.level == "I" and student.gender == "F" and student.status != "Parou")
    total_student_mi = sum(1 for student in students if student.level == "I" and student.gender == "M" and student.status != "Parou")
    total_student_fpro = sum(1 for student in students if student.level == "PRO" and student.gender == "F" and student.status != "Parou")
    total_student_mpro = sum(1 for student in students if student.level == "PRO" and student.gender == "M" and student.status != "Parou")

    # Buscando total de estudantes masculino e feminino
    total_student_m = sum(1 for student in students if student.gender == 'M' and student.status != "Parou")
    total_student_f = sum(1 for student in students if student.gender == 'F' and student.status != "Parou")

    return dict(
        total_student_fa=total_student_fa,
        total_student_ma=total_student_ma,
        total_student_fb=total_student_fb,
        total_student_mb=total_student_mb,
        total_student_fc=total_student_fc,
        total_student_mc=total_student_mc,
        total_student_fd=total_student_fd,
        total_student_md=total_student_md,
        total_student_fi=total_student_fi,
        total_student_mi=total_student_mi,
        total_student_fpro=total_student_fpro,
        total_student_mpro=total_student_mpro,
        total_student_f=total_student_f,
        total_student_m=total_student_m,
    )
