from django.contrib import admin
from proposta.models import Proposta

class PropostaAdmin(admin.ModelAdmin):
    list_display = ['id', 'projeto', 'freelancer', 'preco', 'status', 'data_criacao']
    search_fields = ['projeto__titulo', 'freelancer__nome']
    list_filter = ['status', 'data_criacao']
    
admin.site.register(Proposta, PropostaAdmin)