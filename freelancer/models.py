from django.db import models
from django.contrib.auth.models import User
from freelancer.consts import *

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    papel = models.SmallIntegerField(choices=OPCOES_PAPEIS)
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=100)
    habilidades = models.JSONField()
    bio = models.TextField(blank=True, null=True)
    foto = models.ImageField(blank=True, null=True, upload_to='freelancer/fotos')

    class Meta:
        ordering = ('-id',)