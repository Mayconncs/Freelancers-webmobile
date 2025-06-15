from django.db import models
from django.contrib.auth.models import User
from freelancer.consts import *

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    papel = models.SmallIntegerField(choices=OPCOES_PAPEIS)
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, help_text="Ex: SP, RJ", null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=9, help_text="Formato: 12345-678", null=True, blank=True)
    lote = models.CharField(max_length=50, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True, help_text="Ex: (11) 91234-5678")
    email_contato = models.EmailField(blank=True, null=True)
    habilidades = models.JSONField()
    bio = models.TextField(blank=True, null=True)
    foto = models.ImageField(blank=True, null=True, upload_to='freelancer/fotos')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.nome

    def get_habilidades_display(self):
        return [dict(OPCOES_HABILIDADES).get(h, 'Desconhecido') for h in self.habilidades]