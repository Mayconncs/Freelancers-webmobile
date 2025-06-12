from django.contrib import admin
from projeto.models import Projeto

class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'cliente', 'localizacao', 'status', 'data_criacao']
    search_fields = ['titulo', 'localizacao']
    list_filter = ['status', 'data_criacao']
    
admin.site.register(Projeto, ProjetoAdmin)