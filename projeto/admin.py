from django.contrib import admin
from projeto.models import Projeto

class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'cliente', 'cidade', 'estado', 'status', 'data_criacao']
    search_fields = ['titulo', 'cidade', 'estado']
    list_filter = ['status', 'data_criacao']

admin.site.register(Projeto, ProjetoAdmin)