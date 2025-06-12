from django.urls import path
from projeto.views import *

urlpatterns = [
    path('', ListarProjetos.as_view(), name='listar-projetos'),
    path('novo/', CriarProjeto.as_view(), name='criar-projeto'),
    path('<int:pk>/', EditarProjeto.as_view(), name='editar-projeto'),
    path('deletar/<int:pk>/', DeletarProjeto.as_view(), name='deletar-projeto'),
    path('api/', APIListarProjetos.as_view(), name='api-listar-projetos'),
]