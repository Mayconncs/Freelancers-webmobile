from django.urls import path
from portfolio.views import *

urlpatterns = [
    path('', ListarPortfolios.as_view(), name='listar-portfolios'),
    path('novo/', CriarPortfolio.as_view(), name='criar-portfolio'),
    path('<int:pk>/', EditarPortfolio.as_view(), name='editar-portfolio'),
    path('deletar/<int:pk>/', DeletarPortfolio.as_view(), name='deletar-portfolio'),
    path('api/', APIListarPortfolios.as_view(), name='api-listar-portfolios'),
]