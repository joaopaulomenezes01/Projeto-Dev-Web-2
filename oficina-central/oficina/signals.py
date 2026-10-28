from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import HistoricoOrdem, OrdemServico


@receiver(pre_save, sender=OrdemServico)
def guardar_status_anterior(sender, instance, **kwargs):
    if instance.pk:
        instance._status_anterior = (
            OrdemServico.objects.filter(pk=instance.pk).values_list("status", flat=True).first()
        )
    else:
        instance._status_anterior = None


@receiver(post_save, sender=OrdemServico)
def registrar_historico(sender, instance, created, **kwargs):
    if created or instance._status_anterior != instance.status:
        HistoricoOrdem.objects.create(ordem=instance, status=instance.status)