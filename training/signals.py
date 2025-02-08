from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from . import models

# Variável global para armazenar o valor antigo do local antes da atualização
old_location_cache = {}

# Sinal para capturar o valor antigo do local antes da atualização
@receiver(pre_save, sender=models.TrainingClass)
def capture_old_location(sender, instance, **kwargs):
    if instance.pk:  # Verifica se o objeto já existe no banco de dados (não é uma criação)
        try:
            old_instance = models.TrainingClass.objects.get(pk=instance.pk)
            old_location_cache[instance.pk] = old_instance.location
            print(f"Valor antigo do local capturado: {old_instance.location}")  # Depuração
        except models.TrainingClass.DoesNotExist:
            pass  # Objeto não existe (pode ser uma criação)

# Sinal para atualizar quantity_training quando um treino é criado ou atualizado
@receiver(post_save, sender=models.TrainingClass)
def update_expense_location_training(sender, instance, **kwargs):
    print(f"Treino salvo/atualizado: {instance}")  # Depuração

    # Verifica se é uma atualização e se o local foi alterado
    if instance.pk:  # Se o objeto já existe no banco de dados (não é uma criação)
        old_location = old_location_cache.get(instance.pk)
        new_location = instance.location

        # Se o local foi alterado
        if old_location and old_location != new_location:
            # Decrementa o quantity_training do local antigo (se for maior que 0)
            if old_location.name == "Arena Brasil":
                arena_brasil = models.LocationTraining.objects.get(name='Arena Brasil')
                if arena_brasil.quantity_training > 0:
                    arena_brasil.quantity_training -= 1
                    arena_brasil.save()
                    print(f"Quantidade de treinos na Arena Brasil decrementada: {arena_brasil.quantity_training}")  # Depuração
                else:
                    print("Quantidade de treinos na Arena Brasil já é 0. Não foi decrementada.")  # Depuração

            if old_location.name == "Arena Criciuma":
                arena_criciuma = models.LocationTraining.objects.get(name='Arena Criciuma')
                if arena_criciuma.quantity_training > 0:
                    arena_criciuma.quantity_training -= 1
                    arena_criciuma.save()
                    print(f"Quantidade de treinos na Arena Criciuma decrementada: {arena_criciuma.quantity_training}")  # Depuração
                else:
                    print("Quantidade de treinos na Arena Criciuma já é 0. Não foi decrementada.")  # Depuração

        # Limpa o cache do local antigo
        if instance.pk in old_location_cache:
            del old_location_cache[instance.pk]

    # Incrementa o quantity_training do novo local (ou mantém o mesmo se não houve alteração)
    if instance.location.name == "Arena Brasil":
        arena_brasil = models.LocationTraining.objects.get(name='Arena Brasil')
        arena_brasil.quantity_training += 1
        arena_brasil.save()
        print(f"Quantidade de treinos na Arena Brasil incrementada: {arena_brasil.quantity_training}")  # Depuração

    if instance.location.name == "Arena Criciuma":
        arena_criciuma = models.LocationTraining.objects.get(name='Arena Criciuma')
        arena_criciuma.quantity_training += 1
        arena_criciuma.save()
        print(f"Quantidade de treinos na Arena Criciuma incrementada: {arena_criciuma.quantity_training}")  # Depuração

# Sinal para decrementar quantity_training quando um treino é excluído
@receiver(post_delete, sender=models.TrainingClass)
def remove_expense_location_training(sender, instance, **kwargs):
    print(f"Treino excluído: {instance}")  # Depuração

    if instance.location.name == "Arena Brasil":
        arena_brasil = models.LocationTraining.objects.get(name='Arena Brasil')
        if arena_brasil.quantity_training > 0:
            arena_brasil.quantity_training -= 1
            arena_brasil.save()
            print(f"Quantidade de treinos na Arena Brasil decrementada: {arena_brasil.quantity_training}")  # Depuração
        else:
            print("Quantidade de treinos na Arena Brasil já é 0. Não foi decrementada.")  # Depuração

    if instance.location.name == "Arena Criciuma":
        arena_criciuma = models.LocationTraining.objects.get(name='Arena Criciuma')
        if arena_criciuma.quantity_training > 0:
            arena_criciuma.quantity_training -= 1
            arena_criciuma.save()
            print(f"Quantidade de treinos na Arena Criciuma decrementada: {arena_criciuma.quantity_training}")  # Depuração
        else:
            print("Quantidade de treinos na Arena Criciuma já é 0. Não foi decrementada.")  # Depuração