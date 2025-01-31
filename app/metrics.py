from payment.models import PaymentReceived
from payment.models import PaymentPending
from django.utils.formats import number_format
from django.db.models import Sum
from student.models import Student
from expense.models import Expense
import datetime

# Buscando métricas de pagamentos, total recebido, total de estudante que ja pagaram, valor total a receber e quantidade de alunos que nao pagaram
def get_sales_metric():
    date = datetime.date.today()    
    payment_received = PaymentReceived.objects.all()
    payment_pending = PaymentPending.objects.all()
    expenses = Expense.objects.all()
    total_received = sum(payment.amount_paid for payment in payment_received)
    total_student_received = sum(1 for payment in payment_received if payment.created_at.month == date.month and payment.created_at.year == date.year)
    total_payment_pending = sum(payment.student.value_discount for payment in payment_pending)
    payment_student_pending = sum(1 for payment in payment_pending if payment.created_at.month == date.month)
    expense = sum(expense.value for expense in expenses)

    return dict(
        total_received=number_format(total_received, decimal_pos=2, force_grouping=True),
        total_student_received=total_student_received,
        total_payment_pending=number_format(total_payment_pending, decimal_pos=2, force_grouping=True),
        payment_student_pending=payment_student_pending,
        expense_value = number_format(expense, decimal_pos=2, force_grouping=True),
    )

# Buscando estudantes por categoria e gênero
def get_students_metric():
    students = Student.objects.all()
    # Buscando estudantes por categoria e gênero
    total_student_fa = sum(1 for student in students if student.level == "A" and student.gender == "F" and student.status != "Parou")
    total_student_ma = sum(1 for student in students if student.level == "A" and student.gender == "M" and student.status != "Parou" )
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

