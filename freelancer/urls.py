from django.urls import path
from freelancer.views import *

urlpatterns = [
    path('', ListarFreelancers.as_view(), name='listar-freelancers'),
    path('novo/', CriarPerfil.as_view(), name='criar-perfil'),
    path('<int:pk>/', EditarPerfil.as_view(), name='editar-perfil'),
    path('deletar/<int:pk>/', DeletarPerfil.as_view(), name='deletar-perfil'),
    path('api/', APIListarFreelancers.as_view(), name='api-listar-freelancers'),
    path('fotos/<str:arquivo>/', FotoPerfil.as_view(), name='foto-perfil'),
]