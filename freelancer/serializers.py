from rest_framework import serializers
from freelancer.models import Perfil
from freelancer.consts import *

class SerializadorPerfil(serializers.ModelSerializer):
    nome_papel = serializers.SerializerMethodField()
    nome_habilidades = serializers.SerializerMethodField()

    class Meta:
        model = Perfil
        exclude = []

    def get_nome_papel(self, instancia):
        return instancia.get_papel_display()

    def get_nome_habilidades(self, instancia):
        return [dict(OPCOES_HABILIDADES).get(h, 'Desconhecido') for h in instancia.habilidades]