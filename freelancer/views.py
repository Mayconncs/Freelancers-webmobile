from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from freelancer.models import Perfil
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from freelancer.forms import FormularioPerfil
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from freelancer.serializers import SerializadorPerfil
from django.contrib import messages
from freelancer.consts import OPCOES_PAPEIS
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet

class ListarFreelancers(LoginRequiredMixin, ListView):
    model = Perfil
    context_object_name = 'freelancers'
    template_name = 'freelancer/listar.html'

    def get_queryset(self):
        return Perfil.objects.filter(papel=1)

class DetalharPerfil(LoginRequiredMixin, DetailView):
    model = Perfil
    context_object_name = 'freelancer'
    template_name = 'freelancer/detalhar.html'

class CriarPerfil(LoginRequiredMixin, CreateView):
    model = Perfil
    form_class = FormularioPerfil
    template_name = 'freelancer/novo.html'
    success_url = reverse_lazy('listar-freelancers')

    def get(self, request, *args, **kwargs):
        if Perfil.objects.filter(usuario=request.user).exists():
            messages.error(request, 'Você já possui um perfil! Veja ou edite seu perfil existente.')
            perfil = Perfil.objects.get(usuario=request.user)
            return redirect('detalhar-perfil', pk=perfil.pk)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Perfil criado com sucesso!')
            return response
        except IntegrityError:
            messages.error(self.request, 'Você já possui um perfil! Veja ou edite seu perfil existente.')
            perfil = Perfil.objects.get(usuario=self.request.user)
            return redirect('detalhar-perfil', pk=perfil.pk)

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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.usuario != self.request.user:
            messages.error(self.request, 'Você não tem permissão para editar este perfil.')
            return redirect('listar-freelancers')
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return response

class DeletarPerfil(LoginRequiredMixin, DeleteView):
    model = Perfil
    template_name = 'freelancer/deletar.html'
    success_url = reverse_lazy('listar-freelancers')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.usuario != self.request.user:
            messages.error(self.request, 'Você não tem permissão para deletar este perfil.')
            return redirect('listar-freelancers')
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Perfil deletado com sucesso!')
        return super().delete(request, *args, **kwargs)

class FreelancerViewSet(ModelViewSet):
    serializer_class = SerializadorPerfil
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Perfil.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            return Perfil.objects.filter(papel=1)
        return Perfil.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.usuario != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar este perfil.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.usuario != self.request.user:
            raise PermissionDenied("Você não tem permissão para deletar este perfil.")
        instance.delete()