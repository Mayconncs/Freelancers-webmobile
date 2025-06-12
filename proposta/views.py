from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from proposta.models import Proposta
from proposta.forms import FormularioProposta
from proposta.serializers import SerializadorProposta
from projeto.models import Projeto
from freelancer.consts import OPCOES_HABILIDADES
from django.shortcuts import get_object_or_404
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
        projeto.habilidades_requeridas = [dict(OPCOES_HABILIDADES).get(h, 'Desconhecido') for h in projeto.habilidades_requeridas]
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

class AceitarProposta(LoginRequiredMixin, CreateView):
    model = Proposta
    fields = []

    def post(self, request, *args, **kwargs):
        proposta = Proposta.objects.get(pk=self.kwargs['pk'])
        proposta.status = 2
        proposta.save()
        messages.success(self.request, 'Proposta aceita com sucesso!')
        return self.get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('listar-propostas')

class APIListarPropostas(ListAPIView):
    serializer_class = SerializadorProposta
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Proposta.objects.all()

class APIAceitarProposta(RetrieveUpdateAPIView):
    serializer_class = SerializadorProposta
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Proposta.objects.all()