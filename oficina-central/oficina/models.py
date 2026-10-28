from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="veiculos")
    placa = models.CharField(max_length=8, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["placa"]
        verbose_name = "veículo"

    def __str__(self):
        return f"{self.modelo} ({self.placa})"

class Mecanico(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "mecânico"

    def __str__(self):
        return self.nome

class OrdemServico(models.Model):
    class Status(models.TextChoices):
        ABERTA = "aberta", "Aberta"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        AGUARDANDO_PECA = "aguardando_peca", "Aguardando peça"
        PRONTO = "pronto", "Pronto para retirada"
        CONCLUIDA = "concluida", "Concluída"

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name="ordens")
    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE, related_name="ordens")
    descricao = models.TextField("descrição do serviço")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["-data_abertura"]
        verbose_name = "ordem de serviço"
        verbose_name_plural = "ordens de serviço"

    def __str__(self):
        return f"Ordem #{self.pk:04d}"

    def save(self, *args, **kwargs):
        if self.status == self.Status.CONCLUIDA and not self.data_conclusao:
            self.data_conclusao = timezone.now()
        super().save(*args, **kwargs)
class HistoricoOrdem(models.Model):
    ordem = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name="historico")
    status = models.CharField(max_length=20, choices=OrdemServico.Status.choices)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["data", "id"]
        verbose_name = "histórico da ordem"
        verbose_name_plural = "históricos das ordens"

    def __str__(self):
        return f"{self.ordem} - {self.get_status_display()}"        
class Notificacao(models.Model):
    ordem = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name="notificacoes")
    mensagem = models.CharField(max_length=255)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em", "-id"]
        verbose_name = "notificação"
        verbose_name_plural = "notificações"

    def __str__(self):
        return self.mensagem