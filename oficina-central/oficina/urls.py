from django.urls import path
from django.views.generic import RedirectView

from . import views as v


def crud(prefixo, nome, lista, criar, editar, excluir):
    return [
        path(f"{prefixo}/", lista.as_view(), name=f"{nome}_lista"),
        path(f"{prefixo}/novo/", criar.as_view(), name=f"{nome}_criar"),
        path(f"{prefixo}/<int:pk>/editar/", editar.as_view(), name=f"{nome}_editar"),
        path(f"{prefixo}/<int:pk>/excluir/", excluir.as_view(), name=f"{nome}_excluir"),
    ]


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="ordemservico_lista"), name="home"),
]
urlpatterns += crud("clientes", "cliente", v.ClienteLista, v.ClienteCriar, v.ClienteEditar, v.ClienteExcluir)
urlpatterns += crud("veiculos", "veiculo", v.VeiculoLista, v.VeiculoCriar, v.VeiculoEditar, v.VeiculoExcluir)
urlpatterns += crud("mecanicos", "mecanico", v.MecanicoLista, v.MecanicoCriar, v.MecanicoEditar, v.MecanicoExcluir)
urlpatterns += crud("ordens", "ordemservico", v.OrdemLista, v.OrdemCriar, v.OrdemEditar, v.OrdemExcluir)
urlpatterns += [
    path("ordens/<int:pk>/", v.OrdemDetalhe.as_view(), name="ordemservico_detalhe"),
]
urlpatterns += [
    path("notificacoes/", v.NotificacaoLista.as_view(), name="notificacao_lista"),
]