from unittest import mock

from django.test import TestCase
from django.urls import reverse

from .models import Cliente, HistoricoOrdem, Mecanico, OrdemServico, Veiculo


class FluxoOficinaTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome="Maria Souza", telefone="8199999-0000")
        self.veiculo = Veiculo.objects.create(
            cliente=self.cliente, placa="ABC1D23", marca="Fiat", modelo="Uno", ano=2012
        )
        self.mecanico = Mecanico.objects.create(nome="Carlos")

    def nova_ordem(self, **extra):
        dados = dict(veiculo=self.veiculo, mecanico=self.mecanico, descricao="Troca de óleo")
        dados.update(extra)
        with mock.patch("oficina.signals.publicar_evento"):
            with self.captureOnCommitCallbacks(execute=True):
                return OrdemServico.objects.create(**dados)

    def test_paginas_de_lista_abrem(self):
        for nome in ["cliente", "veiculo", "mecanico", "ordemservico", "notificacao"]:
            resposta = self.client.get(reverse(f"{nome}_lista"))
            self.assertEqual(resposta.status_code, 200, nome)

    def test_crud_de_cliente(self):
        r = self.client.post(reverse("cliente_criar"), {"nome": "João", "telefone": "", "email": ""})
        self.assertRedirects(r, reverse("cliente_lista"))
        novo = Cliente.objects.get(nome="João")
        self.client.post(reverse("cliente_editar", args=[novo.pk]), {"nome": "João P.", "telefone": "", "email": ""})
        novo.refresh_from_db()
        self.assertEqual(novo.nome, "João P.")
        self.client.post(reverse("cliente_excluir", args=[novo.pk]))
        self.assertFalse(Cliente.objects.filter(pk=novo.pk).exists())

    def test_criar_ordem_pela_interface(self):
        with mock.patch("oficina.signals.publicar_evento"):
            r = self.client.post(
                reverse("ordemservico_criar"),
                {
                    "veiculo": self.veiculo.pk,
                    "mecanico": self.mecanico.pk,
                    "descricao": "Freios",
                    "status": "aberta",
                    "valor_estimado": "350.00",
                },
            )
        self.assertRedirects(r, reverse("ordemservico_lista"))
        self.assertEqual(OrdemServico.objects.count(), 1)
    def test_ordem_criada_publica_evento_e_gera_historico(self):
        with mock.patch("oficina.signals.publicar_evento") as publicar:
            with self.captureOnCommitCallbacks(execute=True):
                ordem = OrdemServico.objects.create(
                    veiculo=self.veiculo, mecanico=self.mecanico, descricao="Revisão"
                )
        publicar.assert_called_once_with(ordem)
        self.assertEqual(HistoricoOrdem.objects.filter(ordem=ordem).count(), 1)

    def test_mudar_status_publica_novo_evento(self):
        ordem = self.nova_ordem()
        with mock.patch("oficina.signals.publicar_evento") as publicar:
            with self.captureOnCommitCallbacks(execute=True):
                ordem.status = OrdemServico.Status.PRONTO
                ordem.save()
        publicar.assert_called_once()
        self.assertEqual(ordem.historico.count(), 2)

    def test_salvar_sem_mudar_status_nao_publica(self):
        ordem = self.nova_ordem()
        with mock.patch("oficina.signals.publicar_evento") as publicar:
            with self.captureOnCommitCallbacks(execute=True):
                ordem.descricao = "Outra descrição"
                ordem.save()
        publicar.assert_not_called()
        self.assertEqual(ordem.historico.count(), 1)

    def test_concluir_preenche_data_de_conclusao(self):
        ordem = self.nova_ordem()
        self.assertIsNone(ordem.data_conclusao)
        ordem.status = OrdemServico.Status.CONCLUIDA
        with mock.patch("oficina.signals.publicar_evento"):
            ordem.save()
        self.assertIsNotNone(ordem.data_conclusao)