from django.db import models
from freelancer.models import Perfil
from projeto.consts import *

class Projeto(models.Model):
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='projetos')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    habilidades_requeridas = models.JSONField()
    estado = models.CharField(max_length=2, help_text="Ex: SP, RJ", null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=9, help_text="Formato: 12345-678", null=True, blank=True)
    lote = models.CharField(max_length=50, blank=True, null=True)
    status = models.SmallIntegerField(choices=OPCOES_STATUS)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def get_habilidades_display(self):
        from freelancer.consts import OPCOES_HABILIDADES
        return [dict(OPCOES_HABILIDADES).get(h, 'Desconhecido') for h in self.habilidades_requeridas]