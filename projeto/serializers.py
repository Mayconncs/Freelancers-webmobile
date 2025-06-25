from rest_framework import serializers
from projeto.models import Projeto
from freelancer.models import Perfil

class SerializadorProjeto(serializers.ModelSerializer):
    nome_status = serializers.SerializerMethodField()
    nome_habilidades = serializers.SerializerMethodField()
    cliente_info = serializers.SerializerMethodField()

    class Meta:
        model = Projeto
        fields = ['id', 'cliente', 'cliente_info', 'titulo', 'descricao', 'habilidades_requeridas', 'nome_habilidades',
                  'estado', 'cidade', 'cep', 'lote', 'status', 'nome_status', 'data_criacao']

    def get_nome_status(self, instancia):
        return instancia.get_status_display()

    def get_nome_habilidades(self, instancia):
        from freelancer.consts import OPCOES_HABILIDADES
        return [dict(OPCOES_HABILIDADES).get(h, 'Desconhecido') for h in instancia.habilidades_requeridas]

    def get_cliente_info(self, instancia):
        return {
            'nome': instancia.cliente.nome,
            'telefone': instancia.cliente.telefone or 'Não informado',
            'email_contato': instancia.cliente.email_contato or 'Não informado'
        }