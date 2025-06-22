from django.urls import path, include
from rest_framework.routers import DefaultRouter
from freelancer.views import *

router = DefaultRouter()
router.register(r'api', FreelancerViewSet, basename='freelancer')

urlpatterns = [
    path('', ListarFreelancers.as_view(), name='listar-freelancers'),
    path('novo/', CriarPerfil.as_view(), name='criar-perfil'),
    path('<int:pk>/', DetalharPerfil.as_view(), name='detalhar-perfil'),
    path('editar/<int:pk>/', EditarPerfil.as_view(), name='editar-perfil'),
    path('deletar/<int:pk>/', DeletarPerfil.as_view(), name='deletar-perfil'),
    path('fotos/<str:arquivo>/', FotoPerfil.as_view(), name='foto-perfil'),
    path('', include(router.urls)),
]