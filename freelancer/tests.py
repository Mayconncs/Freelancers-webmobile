from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from freelancer.models import Perfil
from freelancer.forms import FormularioPerfil
from freelancer.consts import OPCOES_HABILIDADES, OPCOES_PAPEIS
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

class TestesModelPerfil(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.perfil = Perfil(
            usuario=self.user,
            papel=1, 
            nome='Teste Freelancer',
            habilidades=[1, 2], 
            estado='SP',
            cidade='São Paulo',
            cep='12345-678',
            telefone='(11) 91234-5678',
            email_contato='teste@exemplo.com',
            bio='Sou um freelancer experiente.'
        )

    def test_get_habilidades_display(self):
        self.assertEqual(
            self.perfil.get_habilidades_display(),
            ['Desenvolvimento Web', 'Design Gráfico']
        )
        self.perfil.habilidades = [99]
        self.assertEqual(self.perfil.get_habilidades_display(), ['Desconhecido'])

    def test_str(self):
        self.assertEqual(str(self.perfil), 'Teste Freelancer')

class TestesViewListarFreelancers(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse('listar-freelancers')
        Perfil.objects.create(
            usuario=User.objects.create_user(username='freelancer1', password='12345'),
            papel=1, nome='Freelancer 1', habilidades=[1]
        )
        Perfil.objects.create(
            usuario=User.objects.create_user(username='cliente1', password='12345'),
            papel=2, nome='Cliente 1', habilidades=[2]
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['freelancers']), 1)
        self.assertEqual(response.context['freelancers'][0].nome, 'Freelancer 1')

class TestesViewCriarPerfil(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse('criar-perfil')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioPerfil)

    def test_post(self):
        data = {
            'papel': 1,
            'nome': 'Novo Freelancer',
            'estado': 'SP',
            'cidade': 'São Paulo',
            'cep': '12345-678',
            'telefone': '(11) 91234-5678',
            'email_contato': 'novo@exemplo.com',
            'habilidades': [1, 2],
            'bio': 'Novo freelancer.'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-freelancers'))
        self.assertEqual(Perfil.objects.count(), 1)
        perfil = Perfil.objects.first()
        self.assertEqual(perfil.nome, 'Novo Freelancer')
        self.assertEqual(perfil.habilidades, [1, 2])

class TestesViewDetalharPerfil(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client = Client()
        self.client.force_login(self.user)
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=1,
            nome='Teste Freelancer',
            habilidades=[1]
        )
        self.url = reverse('detalhar-perfil', kwargs={'pk': self.perfil.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('freelancer'), Perfil)
        self.assertEqual(response.context.get('freelancer').pk, self.perfil.pk)
        self.assertEqual(response.context.get('freelancer').nome, 'Teste Freelancer')

class TestesViewEditarPerfil(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client = Client()
        self.client.force_login(self.user)
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=1,
            nome='Teste Freelancer',
            habilidades=[1]
        )
        self.url = reverse('editar-perfil', kwargs={'pk': self.perfil.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Perfil)
        self.assertIsInstance(response.context.get('form'), FormularioPerfil)
        self.assertEqual(response.context.get('object').pk, self.perfil.pk)
        self.assertEqual(response.context.get('object').nome, 'Teste Freelancer')

    def test_post(self):
        data = {
            'papel': 1,
            'nome': 'Freelancer Editado',
            'estado': 'SP',
            'cidade': 'São Paulo',
            'cep': '12345-678',
            'telefone': '(11) 91234-5678',
            'email_contato': 'editado@exemplo.com',
            'habilidades': [2],
            'bio': 'Perfil editado.'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-freelancers'))
        self.assertEqual(Perfil.objects.count(), 1)
        perfil = Perfil.objects.first()
        self.assertEqual(perfil.nome, 'Freelancer Editado')
        self.assertEqual(perfil.habilidades, [2])
        self.assertEqual(perfil.pk, self.perfil.pk)

class TestesViewDeletarPerfil(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client = Client()
        self.client.force_login(self.user)
        self.perfil = Perfil.objects.create(
            usuario=self.user,
            papel=1,
            nome='Teste Freelancer',
            habilidades=[1]
        )
        self.url = reverse('deletar-perfil', kwargs={'pk': self.perfil.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('object'), Perfil)
        self.assertEqual(response.context.get('object').pk, self.perfil.pk)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-freelancers'))
        self.assertEqual(Perfil.objects.count(), 0)

class TestesAPIFreelancerViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='teste', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        Perfil.objects.create(
            usuario=self.user,
            papel=1, 
            nome='Teste Freelancer',
            habilidades=[1, 2],
            estado='SP',
            cidade='São Paulo',
            cep='12345-678',
            telefone='(11) 91234-5678',
            email_contato='teste@exemplo.com',
            bio='Sou um freelancer experiente.'
        )
        Perfil.objects.create(
            usuario=User.objects.create_user(username='cliente', password='12345'),
            papel=2, 
            nome='Teste Cliente',
            habilidades=[1]
        )
        self.url = reverse('freelancer-list')

    def test_listar_freelancers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Teste Freelancer')
        self.assertEqual(response.data[0]['nome_papel'], 'FREELANCER')
        self.assertEqual(response.data[0]['nome_habilidades'], ['Desenvolvimento Web', 'Design Gráfico'])
        self.assertNotIn('Teste Cliente', [perfil['nome'] for perfil in response.data])