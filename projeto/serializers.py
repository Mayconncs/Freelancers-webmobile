from rest_framework import serializers
from projeto.models import Projeto

class SerializadorProjeto(serializers.ModelSerializer):
    nome_status = serializers.SerializerMethodField()
    nome_habilidades = serializers.SerializerMethodField()

    class Meta:
        model = Projeto
        fields = ['id', 'cliente', 'titulo', 'descricao', 'habilidades_requeridas', 'nome_habilidades',
                  'estado', 'cidade', 'cep', 'lote', 'status', 'nome_status', 'data_criacao']

    def get_nome_status(self, instancia):
        return instancia.get_status_display()

    def get_nome_habilidades(self, instancia):
        from freelancer.consts import OPCOES_HABILIDADES
        return [dict(OPCOES_HABILIDADES).get(h, 'Desconhecido') for h in instancia.habilidades_requeridas]