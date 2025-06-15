from django.contrib import admin
from freelancer.models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'nome', 'papel', 'estado', 'cidade']
    search_fields = ['nome', 'estado', 'cidade', 'email_contato']

admin.site.register(Perfil, PerfilAdmin)