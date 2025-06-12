from django.contrib import admin
from django.urls import path, include
from sistema.views import Login, Logout, LoginAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('freelancer/', include('freelancer.urls'), name='freelancer'),
    path('projeto/', include('projeto.urls'), name='projeto'),
    path('proposta/', include('proposta.urls'), name='proposta'),
    path('portfolio/', include('portfolio.urls'), name='portfolio'),
    path('autenticacao-api/', LoginAPI.as_view(), name='login-api'),
]
