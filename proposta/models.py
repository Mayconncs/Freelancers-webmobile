from django.db import models
from freelancer.models import Perfil
from projeto.models import Projeto
from proposta.consts import *

class Proposta(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='propostas')
    freelancer = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='propostas')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tempo_estimado = models.CharField(max_length=50)
    mensagem = models.TextField()
    status = models.SmallIntegerField(choices=OPCOES_STATUS_PROPOSTA)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)