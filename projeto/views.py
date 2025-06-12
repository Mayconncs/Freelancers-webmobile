from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from projeto.models import Projeto
from projeto.forms import FormularioProjeto
from projeto.serializers import SerializadorProjeto
from freelancer.consts import OPCOES_HABILIDADES

class ListarProjetos(LoginRequiredMixin, ListView):
    model = Projeto
    context_object_name = 'projetos'
    template_name = 'projeto/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for projeto in context['projetos']:
            projeto.habilidades_requeridas = [dict(OPCOES_HABILIDADES).get(h, 'Desconhecido') for h in projeto.habilidades_requeridas]
        return context

class CriarProjeto(LoginRequiredMixin, CreateView):
    model = Projeto
    form_class = FormularioProjeto
    template_name = 'projeto/novo.html'
    success_url = reverse_lazy('listar-projetos')

    def form_valid(self, form):
        form.instance.cliente = self.request.user.perfil
        return super().form_valid(form)

class EditarProjeto(LoginRequiredMixin, UpdateView):
    model = Projeto
    form_class = FormularioProjeto
    template_name = 'projeto/editar.html'
    success_url = reverse_lazy('listar-projetos')

class DeletarProjeto(LoginRequiredMixin, DeleteView):
    model = Projeto
    template_name = 'projeto/deletar.html'
    success_url = reverse_lazy('listar-projetos')

class APIListarProjetos(ListAPIView):
    serializer_class = SerializadorProjeto
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Projeto.objects.all()