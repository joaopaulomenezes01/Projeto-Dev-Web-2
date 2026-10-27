from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ClienteForm, MecanicoForm, VeiculoForm
from .models import Cliente, Mecanico, Veiculo


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