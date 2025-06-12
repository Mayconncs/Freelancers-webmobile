from django.contrib import admin
from freelancer.models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'nome', 'papel', 'localizacao']
    search_fields = ['nome', 'localizacao']

admin.site.register(Perfil, PerfilAdmin)