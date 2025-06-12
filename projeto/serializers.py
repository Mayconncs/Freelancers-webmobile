from rest_framework import serializers
from projeto.models import Projeto

class SerializadorProjeto(serializers.ModelSerializer):
    nome_status = serializers.SerializerMethodField()
    nome_habilidades = serializers.SerializerMethodField()

    class Meta:
        model = Projeto
        exclude = []

    def get_nome_status(self, instancia):
        return instancia.get_status_display()

    def get_nome_habilidades(self, instancia):
        from freelancer.consts import OPCOES_HABILIDADES
        return [dict(OPCOES_HABILIDADES).get(h, 'Desconhecido') for h in instancia.habilidades_requeridas]