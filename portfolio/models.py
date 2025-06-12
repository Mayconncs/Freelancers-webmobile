from django.db import models
from freelancer.models import Perfil

class Portfolio(models.Model):
    freelancer = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='portfolios')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagens = models.ImageField(blank=True, null=True, upload_to='portfolio/imagens')
    links = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ('-id',)