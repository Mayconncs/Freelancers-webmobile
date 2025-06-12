from django.db import models
from freelancer.models import Perfil
from projeto.consts import *

class Projeto(models.Model):
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='projetos')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    habilidades_requeridas = models.JSONField()
    localizacao = models.CharField(max_length=100)
    status = models.SmallIntegerField(choices=OPCOES_STATUS)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)