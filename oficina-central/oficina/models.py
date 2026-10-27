from django.db import models


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