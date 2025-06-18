from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from proposta.models import Proposta
from proposta.forms import FormularioProposta
from proposta.serializers import SerializadorProposta
from projeto.models import Projeto
from freelancer.consts import OPCOES_HABILIDADES
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class CriarProposta(LoginRequiredMixin, CreateView):
    model = Proposta
    form_class = FormularioProposta
    template_name = 'proposta/novo.html'

    def get_initial(self):
        return {'projeto': self.kwargs['projeto_id']}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projeto = get_object_or_404(Projeto, pk=self.kwargs['projeto_id'])
        context['projeto'] = projeto
        return context

    def form_valid(self, form):
        form.instance.freelancer = self.request.user.perfil
        form.instance.status = 1
        response = super().form_valid(form)
        messages.success(self.request, 'Proposta enviada com sucesso!')
        return response

    def get_success_url(self):
        return reverse_lazy('listar-propostas')

class ListarPropostas(LoginRequiredMixin, ListView):
    model = Proposta
    context_object_name = 'propostas'
    template_name = 'proposta/listar.html'

class DetalharProposta(LoginRequiredMixin, DetailView):
    model = Proposta
    context_object_name = 'proposta'
    template_name = 'proposta/detalhar.html'

class APIListarPropostas(ListAPIView):
    serializer_class = SerializadorProposta
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Proposta.objects.all()
