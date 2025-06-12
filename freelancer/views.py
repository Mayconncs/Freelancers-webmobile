from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from django.views import View
from freelancer.models import Perfil
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from freelancer.forms import FormularioPerfil
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from freelancer.serializers import SerializadorPerfil

class ListarFreelancers(LoginRequiredMixin, ListView):
    model = Perfil
    context_object_name = 'freelancers'
    template_name = 'freelancer/listar.html'

class CriarPerfil(LoginRequiredMixin, CreateView):
    model = Perfil
    form_class = FormularioPerfil
    template_name = 'freelancer/novo.html'
    success_url = reverse_lazy('listar-freelancers')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class FotoPerfil(View):
    def get(self, request, arquivo):
        try:
            perfil = Perfil.objects.get(foto='freelancer/fotos/{}'.format(arquivo))
            return FileResponse(perfil.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada ou acesso não autorizado")
        except Exception as exception:
            raise exception

class EditarPerfil(LoginRequiredMixin, UpdateView):
    model = Perfil
    form_class = FormularioPerfil
    template_name = 'freelancer/editar.html'
    success_url = reverse_lazy('listar-freelancers')

class DeletarPerfil(LoginRequiredMixin, DeleteView):
    model = Perfil
    template_name = 'freelancer/deletar.html'
    success_url = reverse_lazy('listar-freelancers')

class APIListarFreelancers(ListAPIView):
    serializer_class = SerializadorPerfil
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Perfil.objects.all()