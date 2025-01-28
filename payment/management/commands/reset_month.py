from django.core.management.base import BaseCommand
from payment.models import PendingPayment
import calendar
import datetime


class Command(BaseCommand):
    help = "Exibe a quantidade de dias do mês atual."

    def handle(self, *args, **kwargs):
        day = datetime.datetime.today()  # Obtém a data atual
        
        calendario = calendar.monthcalendar(day.year, day.month)
        
        calendar_list = [dia for semana in calendario for dia in semana if dia != 0]
        
        if day.day == calendar_list[-4] and day.hour == 10:
            PendingPayment.objects.all().delete()
            print("Lista renovada com, sucesso")
        else:
            print("Nenhuma ação realizada ")


        self.stdout.write(f'O mês de {day.strftime("%B")} possui {calendar_list[-1]} dias.')

