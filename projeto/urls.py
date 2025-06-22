from django.urls import path, include
from rest_framework.routers import DefaultRouter
from projeto.views import *

router = DefaultRouter()
router.register(r'api', ProjetoViewSet, basename='projeto')

urlpatterns = [
    path('', ListarProjetos.as_view(), name='listar-projetos'),
    path('novo/', CriarProjeto.as_view(), name='criar-projeto'),
    path('detalhar/<int:pk>/', DetalharProjeto.as_view(), name='detalhar-projeto'),
    path('editar/<int:pk>/', EditarProjeto.as_view(), name='editar-projeto'),
    path('deletar/<int:pk>/', DeletarProjeto.as_view(), name='deletar-projeto'),
    path('propostas/<int:projeto_id>/', ListarPropostasPorProjeto.as_view(), name='listar-propostas-por-projeto'),
    path('', include(router.urls)),
]