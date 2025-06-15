from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from projeto.models import Projeto
from projeto.forms import FormularioProjeto
from projeto.serializers import SerializadorProjeto
from django.shortcuts import redirect
from django.contrib import messages
from proposta.models import Proposta
from proposta.serializers import SerializadorProposta

class ListarProjetos(LoginRequiredMixin, ListView):
    model = Projeto
    context_object_name = 'projetos'
    template_name = 'projeto/listar.html'

    def get_queryset(self):
        status_filter = self.request.GET.get('status', 'ativos')
        if status_filter == 'concluidos':
            return Projeto.objects.filter(status=3) 
        return Projeto.objects.filter(status__in=[1, 2])  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', 'ativos')
        return context

class CriarProjeto(LoginRequiredMixin, CreateView):
    model = Projeto
    form_class = FormularioProjeto
    template_name = 'projeto/novo.html'
    success_url = reverse_lazy('listar-projetos')

    def form_valid(self, form):
        form.instance.cliente = self.request.user.perfil
        response = super().form_valid(form)
        messages.success(self.request, 'Projeto criado com sucesso!')
        return response

class DetalharProjeto(LoginRequiredMixin, DetailView):
    model = Projeto
    context_object_name = 'projeto'
    template_name = 'projeto/detalhar.html'

class EditarProjeto(LoginRequiredMixin, UpdateView):
    model = Projeto
    form_class = FormularioProjeto
    template_name = 'projeto/editar.html'
    success_url = reverse_lazy('listar-projetos')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.cliente != self.request.user.perfil:
            messages.error(self.request, 'Você não tem permissão para editar este projeto.')
            return redirect('listar-projetos')
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Projeto atualizado com sucesso!')
        return response

class DeletarProjeto(LoginRequiredMixin, DeleteView):
    model = Projeto
    template_name = 'projeto/deletar.html'
    success_url = reverse_lazy('listar-projetos')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.cliente != self.request.user.perfil:
            messages.error(self.request, 'Você não tem permissão para deletar este projeto.')
            return redirect('listar-projetos')
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Projeto deletado com sucesso!')
        return super().delete(request, *args, **kwargs)

class ListarPropostasPorProjeto(LoginRequiredMixin, ListView):
    model = Proposta
    context_object_name = 'propostas'
    template_name = 'projeto/propostas_por_projeto.html'

    def get_queryset(self):
        projeto_id = self.kwargs['projeto_id']
        return Proposta.objects.filter(projeto_id=projeto_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projeto'] = Projeto.objects.get(pk=self.kwargs['projeto_id'])
        return context

class APIListarProjetos(ListAPIView):
    serializer_class = SerializadorProjeto
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_filter = self.request.GET.get('status', 'ativos')
        if status_filter == 'concluidos':
            return Projeto.objects.filter(status=3)
        return Projeto.objects.filter(status__in=[1, 2])