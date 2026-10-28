from django.contrib import admin

from .models import Cliente, HistoricoOrdem, Mecanico, Notificacao, OrdemServico, Veiculo

admin.site.register([Cliente, Veiculo, Mecanico, OrdemServico, HistoricoOrdem, Notificacao])