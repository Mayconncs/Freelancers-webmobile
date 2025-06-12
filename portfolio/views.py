from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from portfolio.models import Portfolio
from portfolio.forms import FormularioPortfolio
from portfolio.serializers import SerializadorPortfolio

class ListarPortfolios(LoginRequiredMixin, ListView):
    model = Portfolio
    context_object_name = 'portfolios'
    template_name = 'portfolio/listar.html'

class CriarPortfolio(LoginRequiredMixin, CreateView):
    model = Portfolio
    form_class = FormularioPortfolio
    template_name = 'portfolio/novo.html'
    success_url = reverse_lazy('listar-portfolios')

    def form_valid(self, form):
        form.instance.freelancer = self.request.user.perfil
        return super().form_valid(form)

class EditarPortfolio(LoginRequiredMixin, UpdateView):
    model = Portfolio
    form_class = FormularioPortfolio
    template_name = 'portfolio/editar.html'
    success_url = reverse_lazy('listar-portfolios')

class DeletarPortfolio(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolio/deletar.html'
    success_url = reverse_lazy('listar-portfolios')

class APIListarPortfolios(ListAPIView):
    serializer_class = SerializadorPortfolio
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.all()