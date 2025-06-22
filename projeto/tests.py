from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from projeto.models import Projeto
from projeto.forms import FormularioProjeto
from freelancer.models import Perfil
from freelancer.consts import OPCOES_PAPEIS, OPCOES_HABILIDADES
from rest_framework.test import APIClient
import json

class TestesModelProjeto(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=2, 
            nome='Cliente Teste',
            habilidades=[1]
        )
        self.projeto = Projeto(
            cliente=self.perfil,
            titulo='Projeto Teste',
            descricao='Descrição do projeto.',
            habilidades_requeridas=[1, 2],  
            estado='SP',
            cidade='São Paulo',
            cep='12345-678',
            status=1, 
            lote='Lote 123'
        )
        self.projeto.save()

    def test_get_habilidades_display(self):
        self.assertEqual(
            self.projeto.get_habilidades_display(),
            ['Desenvolvimento Web', 'Design Gráfico']
        )
        self.projeto.habilidades_requeridas = [99]
        self.projeto.save()
        self.assertEqual(self.projeto.get_habilidades_display(), ['Desconhecido'])

    def test_str(self):
        self.assertEqual(str(self.projeto), 'Projeto Teste')

    def test_str_with_unicode(self):
        self.projeto.titulo = 'Projeto Ágil'
        self.projeto.save()
        self.assertEqual(str(self.projeto), 'Projeto Ágil')

class TestesViewListarProjetos(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse('listar-projetos')
        Projeto.objects.create(
            cliente=self.perfil,
            titulo='Projeto Pendente',
            descricao='Teste',
            habilidades_requeridas=[1],
            status=1
        )
        Projeto.objects.create(
            cliente=self.perfil,
            titulo='Projeto Em Andamento',
            descricao='Teste',
            habilidades_requeridas=[2],
            status=2
        )
        Projeto.objects.create(
            cliente=self.perfil,
            titulo='Projeto Concluído',
            descricao='Teste',
            habilidades_requeridas=[3],
            status=3
        )

    def test_get_ativos(self):
        response = self.client.get(self.url, {'status': 'ativos'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['projetos']), 2)
        titulos = [projeto.titulo for projeto in response.context['projetos']]
        self.assertIn('Projeto Pendente', titulos)
        self.assertIn('Projeto Em Andamento', titulos)
        self.assertEqual(response.context['status_filter'], 'ativos')

    def test_get_concluidos(self):
        response = self.client.get(self.url, {'status': 'concluidos'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['projetos']), 1)
        self.assertEqual(response.context['projetos'][0].titulo, 'Projeto Concluído')
        self.assertEqual(response.context['status_filter'], 'concluidos')

class TestesViewCriarProjeto(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse('criar-projeto')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioProjeto)

    def test_post(self):
        data = {
            'titulo': 'Novo Projeto',
            'descricao': 'Descrição do projeto.',
            'habilidades_requeridas': [1, 2],
            'estado': 'SP',
            'cidade': 'São Paulo',
            'cep': '12345-678',
            'lote': 'Lote 123',
            'status': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-projetos'))
        self.assertEqual(Projeto.objects.count(), 1)
        projeto = Projeto.objects.first()
        self.assertEqual(projeto.titulo, 'Novo Projeto')
        self.assertEqual(projeto.habilidades_requeridas, [1, 2])
        self.assertEqual(projeto.cliente, self.perfil)

class TestesViewDetalharProjeto(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.projeto = Projeto.objects.create(
            cliente=self.perfil,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1
        )
        self.url = reverse('detalhar-projeto', kwargs={'pk': self.projeto.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('projeto'), Projeto)
        self.assertEqual(response.context.get('projeto').pk, self.projeto.pk)
        self.assertEqual(response.context.get('projeto').titulo, 'Projeto Teste')

class TestesViewEditarProjeto(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.projeto = Projeto.objects.create(
            cliente=self.perfil,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1
        )
        self.url = reverse('editar-projeto', kwargs={'pk': self.projeto.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Projeto)
        self.assertIsInstance(response.context.get('form'), FormularioProjeto)
        self.assertEqual(response.context.get('object').pk, self.projeto.pk)
        self.assertEqual(response.context.get('object').titulo, 'Projeto Teste')

    def test_post(self):
        data = {
            'titulo': 'Projeto Editado',
            'descricao': 'Descrição editada.',
            'habilidades_requeridas': [2],
            'estado': 'RJ',
            'cidade': 'Rio de Janeiro',
            'cep': '98765-432',
            'lote': 'Lote 456',
            'status': 2
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-projetos'))
        self.assertEqual(Projeto.objects.count(), 1)
        projeto = Projeto.objects.first()
        self.assertEqual(projeto.titulo, 'Projeto Editado')
        self.assertEqual(projeto.habilidades_requeridas, [2])
        self.assertEqual(projeto.status, 2)
        self.assertEqual(projeto.pk, self.projeto.pk)

    def test_post_sem_permissao(self):
        outro_user = User.objects.create_user(username='outro', password='12345')
        outro_perfil = Perfil.objects.create(
            usuario=outro_user,
            papel=2, nome='Outro Cliente', habilidades=[1]
        )
        self.client.force_login(outro_user)
        data = {
            'titulo': 'Tentativa de Edição',
            'descricao': 'Descrição.',
            'habilidades_requeridas': [1],
            'status': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 404)
        projeto = Projeto.objects.get(pk=self.projeto.pk)
        self.assertEqual(projeto.titulo, 'Projeto Teste')

class TestesViewDeletarProjeto(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.projeto = Projeto.objects.create(
            cliente=self.perfil,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1
        )
        self.url = reverse('deletar-projeto', kwargs={'pk': self.projeto.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Projeto)
        self.assertEqual(response.context.get('object').pk, self.projeto.pk)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-projetos'))
        self.assertEqual(Projeto.objects.count(), 0)

    def test_post_sem_permissao(self):
        outro_user = User.objects.create_user(username='outro', password='12345')
        outro_perfil = Perfil.objects.create(
            usuario=outro_user,
            papel=2, nome='Outro Cliente', habilidades=[1]
        )
        self.client.force_login(outro_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Projeto.objects.count(), 1)

class TestesViewListarPropostasPorProjeto(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.perfil_cliente = Perfil.objects.create(
            usuario=self.user,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.perfil_freelancer = Perfil.objects.create(
            usuario=User.objects.create_user(username='freelancer', password='12345'),
            papel=1, nome='Freelancer Teste', habilidades=[1]
        )
        self.projeto = Projeto.objects.create(
            cliente=self.perfil_cliente,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse('listar-propostas-por-projeto', kwargs={'projeto_id': self.projeto.pk})
        from proposta.models import Proposta
        Proposta.objects.create(
            projeto=self.projeto,
            freelancer=self.perfil_freelancer,
            preco=1000.00,
            tempo_estimado='5 dias',
            status=1
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['propostas']), 1)
        self.assertEqual(response.context['propostas'][0].freelancer.nome, 'Freelancer Teste')
        self.assertEqual(response.context['projeto'].pk, self.projeto.pk)