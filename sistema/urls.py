from django.contrib import admin
from django.urls import path, include
from sistema.views import Login, Logout, Cadastro, LoginAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('cadastro/', Cadastro.as_view(), name='cadastro'),
    path('logout/', Logout.as_view(), name='logout'),
    path('freelancer/', include('freelancer.urls'), name='freelancer'),
    path('projeto/', include('projeto.urls'), name='projeto'),
    path('proposta/', include('proposta.urls'), name='proposta'),
    path('autenticacao-api/', LoginAPI.as_view(), name='login-api'),
]