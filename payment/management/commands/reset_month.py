from django.core.management.base import BaseCommand
from payment.models import Student
import calendar
import datetime

# Comando para mudar o valor de student.status_payment para pendente quando chegar no ultimo dia do mês as 00 horas, pois é atraves do campo de status de payment que atualizamos a tela de pagamento pendentes
class Command(BaseCommand):
    help = "Exibe a quantidade de dias do mês atual."

    def handle(self, *args, **kwargs):
        day = datetime.datetime.today()  # Obtém a data atual
        
        calendario = calendar.monthcalendar(day.year, day.month)
        
        calendar_list = [dia for semana in calendario for dia in semana if dia != 0]
        
        if day.day == calendar_list[-1] and day.hour == 00:
            students = Student.objects.filter(status_payment = 'pago')
            for student in students:
                if student.status != 'Parou':
                    student.status_payment = 'pendente'
                    student.save()

