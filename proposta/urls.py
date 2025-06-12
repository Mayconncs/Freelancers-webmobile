from django.urls import path
from proposta.views import *

urlpatterns = [
    path('', ListarPropostas.as_view(), name='listar-propostas'),
    path('novo/<int:projeto_id>/', CriarProposta.as_view(), name='criar-proposta'),
    path('aceitar/<int:pk>/', AceitarProposta.as_view(), name='aceitar-proposta'),
    path('api/', APIListarPropostas.as_view(), name='api-listar-propostas'),
]