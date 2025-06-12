from rest_framework import serializers
from proposta.models import Proposta

class SerializadorProposta(serializers.ModelSerializer):
    nome_status = serializers.SerializerMethodField()

    class Meta:
        model = Proposta
        exclude = []

    def get_nome_status(self, instancia):
        return instancia.get_status_display()