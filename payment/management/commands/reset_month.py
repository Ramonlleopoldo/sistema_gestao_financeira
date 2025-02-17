from django.core.management.base import BaseCommand
from student.models import Student
from payment.models import PaymentPending, PaymentDelay
import calendar
import datetime


class Command(BaseCommand):
    help = "Atualiza o status de pagamento dos alunos para 'pendente' ao chegar no último dia do mês."

    def handle(self, *args, **kwargs):
        day = datetime.datetime.today()  # Obtém a data atual
        calendario = calendar.monthcalendar(day.year, day.month)  # Obtém o calendário do mês atual

        # Lista de dias do mês (sem valores 0, que representam dias fora do mês)
        calendar_list = [dia for semana in calendario for dia in semana if dia != 0]
        # Verifica se é o último dia do mês e se a hora é 00
        if day.day == calendar_list[-1] and day.hour == 00:

            # Verificar se há pagamentos pendentes e, se houver, registrar os atrasos
            if PaymentPending.objects.exists():
                for payment in PaymentPending.objects.all():
                    # Criando um novo registro de atraso de pagamento para cada aluno
                    payment_delay = PaymentDelay(student=payment.student,
                                                 value_delay=payment.student.value_discount,
                                                 date=payment.created_at.month)
                    payment_delay.save()

            # Atualizar os alunos com status 'pago' para 'pendente'
            students = Student.objects.filter(status_payment='pago')  # Filtra os alunos com pagamento 'pago'

            for student in students:
                # Verifica se o status do aluno não é 'Parou' antes de atualizar
                if student.status != 'Parou':
                    # Atualiza o status do aluno para 'pendente'
                    student.status_payment = 'pendente'
                    student.save()

            self.stdout.write(self.style.SUCCESS('Status de pagamento atualizado para "pendente" para todos os alunos pagos.'))
