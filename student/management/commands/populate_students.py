from django.core.management.base import BaseCommand
from student.models import Student, GENDER_CHOICES, CLASS_DAYS_CHOICES, BILLING_METHOD_CHOICES, LEVEL_CHOICES, STATUS_CHOICES  # Substitua 'myapp' pelo nome real do seu app
from payment.models import PaymentPending
import random
from decimal import Decimal
from faker import Faker

fake = Faker("pt_BR")

def random_choice(choices):
    return random.choice([choice[0] for choice in choices])

class Command(BaseCommand):
    help = "Popula o banco de dados com 50 estudantes para testes e cria pagamentos pendentes"

    def handle(self, *args, **kwargs):
        students = []
        for _ in range(50):
            student = Student(
                name=fake.name(),
                gender=random_choice(GENDER_CHOICES),
                class_days=", ".join(random.sample([c[0] for c in CLASS_DAYS_CHOICES], random.randint(1, 3))),
                class_quantity=random.randint(1, 20),
                billing_method=random_choice(BILLING_METHOD_CHOICES),
                class_price=Decimal(random.randint(30, 150)),
                monthly_fee=Decimal(random.randint(100, 500)),
                discount=0,
                phone_number=fake.phone_number(),
                level=random_choice(LEVEL_CHOICES),
                due_date=random.randint(1, 28),
                status=random_choice(STATUS_CHOICES),
                status_payment="pendente",
                notes="Aluno gerado automaticamente para testes."
            )
            students.append(student)
        
        created_students = Student.objects.bulk_create(students)
        
        payments = [
            PaymentPending(student=student)
            for student in created_students if student.status_payment == 'pendente'
        ]
        PaymentPending.objects.bulk_create(payments)
        
        self.stdout.write(self.style.SUCCESS("Banco de dados populado com 50 estudantes e pagamentos pendentes criados."))

