from django.db import models
from simple_history.models import HistoricalRecords

class Onibus(models.Model):
    numero = models.CharField(max_length=10, default='SN')
    placa = models.CharField(max_length=10, unique=True)
    capacidade = models.IntegerField()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.numero} - {self.placa}"

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, unique=True)
    cpf =models.CharField(max_length=11, unique=True)
    onibus = models.ForeignKey(Onibus, on_delete=models.SET_NULL, null=True, blank=True)

    history = HistoricalRecords()

class ViagemCliente(models.Model):
    data = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    onibus = models.ForeignKey(Onibus, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20)
    
    history = HistoricalRecords()

class Viagem(models.Model):
    data = models.DateField()
    status = models.CharField(max_length=20)
    hora_de_confirmacao = models.DateTimeField()

    history = HistoricalRecords()