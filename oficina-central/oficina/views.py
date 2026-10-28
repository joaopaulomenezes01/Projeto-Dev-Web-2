from django.urls import reverse
from django.db.models import Q
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView

from .forms import ClienteForm, MecanicoForm, OrdemForm, VeiculoForm
from .models import Cliente, Mecanico, Notificacao, OrdemServico, Veiculo


class VoltaParaLista:
    def get_success_url(self):
        return reverse(f"{self.model._meta.model_name}_lista")


class SalvarMixin(VoltaParaLista):
    template_name = "oficina/form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        acao = "Editar" if self.object else "Novo"
        ctx["titulo"] = f"{acao} {self.model._meta.verbose_name}"
        return ctx


class ExcluirMixin(VoltaParaLista):
    template_name = "oficina/confirmar_exclusao.html"


class ClienteLista(ListView):
    model = Cliente


class ClienteCriar(SalvarMixin, CreateView):
    model = Cliente
    form_class = ClienteForm


class ClienteEditar(SalvarMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm


class ClienteExcluir(ExcluirMixin, DeleteView):
    model = Cliente

class VeiculoLista(ListView):
    model = Veiculo
    queryset = Veiculo.objects.select_related("cliente")


class VeiculoCriar(SalvarMixin, CreateView):
    model = Veiculo
    form_class = VeiculoForm


class VeiculoEditar(SalvarMixin, UpdateView):
    model = Veiculo
    form_class = VeiculoForm


class VeiculoExcluir(ExcluirMixin, DeleteView):
    model = Veiculo

class MecanicoLista(ListView):
    model = Mecanico


class MecanicoCriar(SalvarMixin, CreateView):
    model = Mecanico
    form_class = MecanicoForm


class MecanicoEditar(SalvarMixin, UpdateView):
    model = Mecanico
    form_class = MecanicoForm


class MecanicoExcluir(ExcluirMixin, DeleteView):
    model = Mecanico

class OrdemLista(ListView):
    model = OrdemServico

    def get_queryset(self):
        qs = OrdemServico.objects.select_related("veiculo__cliente", "mecanico")
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")
        if q:
            qs = qs.filter(
                Q(descricao__icontains=q)
                | Q(veiculo__placa__icontains=q)
                | Q(veiculo__cliente__nome__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["status_choices"] = OrdemServico.Status.choices
        contexto["q"] = self.request.GET.get("q", "")
        contexto["status_atual"] = self.request.GET.get("status", "")
        return contexto


class OrdemCriar(SalvarMixin, CreateView):
    model = OrdemServico
    form_class = OrdemForm


class OrdemEditar(SalvarMixin, UpdateView):
    model = OrdemServico
    form_class = OrdemForm


class OrdemExcluir(ExcluirMixin, DeleteView):
    model = OrdemServico

class OrdemDetalhe(DetailView):
    model = OrdemServico
    queryset = OrdemServico.objects.select_related("veiculo__cliente", "mecanico")

class NotificacaoLista(ListView):
    model = Notificacao
    queryset = Notificacao.objects.select_related("ordem")