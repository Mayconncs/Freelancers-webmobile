from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from proposta.models import Proposta
from proposta.forms import FormularioProposta
from projeto.models import Projeto
from freelancer.models import Perfil
from freelancer.consts import OPCOES_PAPEIS
from rest_framework.test import APIClient
import json

class TestesModelProposta(TestCase):
    def setUp(self):
        self.user_freelancer = User.objects.create_user(username='freelancer', password='12345')
        self.perfil_freelancer = Perfil.objects.create(
            usuario=self.user_freelancer,
            papel=1, 
            nome='Freelancer Teste',
            habilidades=[1]
        )
        self.user_cliente = User.objects.create_user(username='cliente', password='12345')
        self.perfil_cliente = Perfil.objects.create(
            usuario=self.user_cliente,
            papel=2, 
            nome='Cliente Teste',
            habilidades=[1]
        )
        self.projeto = Projeto.objects.create(
            cliente=self.perfil_cliente,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1 
        )
        self.proposta = Proposta(
            projeto=self.projeto,
            freelancer=self.perfil_freelancer,
            preco=1000.00,
            tempo_estimado='5 dias',
            mensagem='Proposta de teste.',
            status=1 
        )
        self.proposta.save()

    def test_str(self):
        self.assertEqual(str(self.proposta), f'Proposta object ({self.proposta.pk})')

class TestesFormularioProposta(TestCase):
    def setUp(self):
        self.user_cliente = User.objects.create_user(username='cliente', password='12345')
        self.perfil_cliente = Perfil.objects.create(
            usuario=self.user_cliente,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.projeto_pendente = Projeto.objects.create(
            cliente=self.perfil_cliente,
            titulo='Projeto Pendente',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1 
        )
        self.projeto_fechado = Projeto.objects.create(
            cliente=self.perfil_cliente,
            titulo='Projeto Fechado',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=2 
        )

    def test_form_valido(self):
        data = {
            'projeto': self.projeto_pendente.pk,
            'preco': 1000.00,
            'tempo_estimado': '5 dias',
            'mensagem': 'Proposta válida.'
        }
        form = FormularioProposta(data=data)
        self.assertTrue(form.is_valid())

    def test_form_projeto_fechado(self):
        data = {
            'projeto': self.projeto_fechado.pk,
            'preco': 1000.00,
            'tempo_estimado': '5 dias',
            'mensagem': 'Proposta inválida.'
        }
        form = FormularioProposta(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Propostas só podem ser enviadas para projetos abertos.', form.errors['__all__'])

class TestesViewListarPropostas(TestCase):
    def setUp(self):
        self.user_freelancer = User.objects.create_user(username='freelancer', password='12345')
        self.perfil_freelancer = Perfil.objects.create(
            usuario=self.user_freelancer,
            papel=1, nome='Freelancer Teste', habilidades=[1]
        )
        self.user_cliente = User.objects.create_user(username='cliente', password='12345')
        self.perfil_cliente = Perfil.objects.create(
            usuario=self.user_cliente,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.projeto = Projeto.objects.create(
            cliente=self.perfil_cliente,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1
        )
        self.client = Client()
        self.client.force_login(self.user_freelancer)
        self.url = reverse('listar-propostas')
        Proposta.objects.create(
            projeto=self.projeto,
            freelancer=self.perfil_freelancer,
            preco=1000.00,
            tempo_estimado='5 dias',
            mensagem='Proposta de teste.',
            status=1
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['propostas']), 1)
        self.assertEqual(response.context['propostas'][0].freelancer.nome, 'Freelancer Teste')

class TestesViewCriarProposta(TestCase):
    def setUp(self):
        self.user_freelancer = User.objects.create_user(username='freelancer', password='12345')
        self.perfil_freelancer = Perfil.objects.create(
            usuario=self.user_freelancer,
            papel=1, nome='Freelancer Teste', habilidades=[1]
        )
        self.user_cliente = User.objects.create_user(username='cliente', password='12345')
        self.perfil_cliente = Perfil.objects.create(
            usuario=self.user_cliente,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.projeto = Projeto.objects.create(
            cliente=self.perfil_cliente,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1
        )
        self.client = Client()
        self.client.force_login(self.user_freelancer)
        self.url = reverse('criar-proposta', kwargs={'projeto_id': self.projeto.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioProposta)
        self.assertEqual(response.context.get('projeto').pk, self.projeto.pk)
        self.assertEqual(response.context['form'].initial['projeto'], self.projeto.pk)

    def test_post(self):
        data = {
            'projeto': self.projeto.pk,
            'preco': 1000.00,
            'tempo_estimado': '5 dias',
            'mensagem': 'Proposta de teste.'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar-propostas'))
        self.assertEqual(Proposta.objects.count(), 1)
        proposta = Proposta.objects.first()
        self.assertEqual(proposta.preco, 1000.00)
        self.assertEqual(proposta.tempo_estimado, '5 dias')
        self.assertEqual(proposta.freelancer, self.perfil_freelancer)
        self.assertEqual(proposta.status, 1)

    def test_post_projeto_fechado(self):
        self.projeto.status = 2 
        self.projeto.save()
        data = {
            'projeto': self.projeto.pk,
            'preco': 1000.00,
            'tempo_estimado': '5 dias',
            'mensagem': 'Proposta inválida.'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200) 
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Proposta.objects.count(), 0)

class TestesViewDetalharProposta(TestCase):
    def setUp(self):
        self.user_freelancer = User.objects.create_user(username='freelancer', password='12345')
        self.perfil_freelancer = Perfil.objects.create(
            usuario=self.user_freelancer,
            papel=1, nome='Freelancer Teste', habilidades=[1]
        )
        self.user_cliente = User.objects.create_user(username='cliente', password='12345')
        self.perfil_cliente = Perfil.objects.create(
            usuario=self.user_cliente,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.projeto = Projeto.objects.create(
            cliente=self.perfil_cliente,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1
        )
        self.proposta = Proposta.objects.create(
            projeto=self.projeto,
            freelancer=self.perfil_freelancer,
            preco=1000.00,
            tempo_estimado='5 dias',
            mensagem='Proposta de teste.',
            status=1
        )
        self.client = Client()
        self.client.force_login(self.user_freelancer)
        self.url = reverse('detalhar-proposta', kwargs={'pk': self.proposta.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('proposta'), Proposta)
        self.assertEqual(response.context.get('proposta').pk, self.proposta.pk)
        self.assertEqual(response.context.get('proposta').preco, 1000.00)

class TestesAPIListarPropostas(TestCase):
    def setUp(self):
        self.user_freelancer = User.objects.create_user(username='freelancer', password='12345')
        self.perfil_freelancer = Perfil.objects.create(
            usuario=self.user_freelancer,
            papel=1, nome='Freelancer Teste', habilidades=[1]
        )
        self.user_cliente = User.objects.create_user(username='cliente', password='12345')
        self.perfil_cliente = Perfil.objects.create(
            usuario=self.user_cliente,
            papel=2, nome='Cliente Teste', habilidades=[1]
        )
        self.projeto = Projeto.objects.create(
            cliente=self.perfil_cliente,
            titulo='Projeto Teste',
            descricao='Descrição',
            habilidades_requeridas=[1],
            status=1
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_freelancer)
        self.url = reverse('api-listar-propostas')
        Proposta.objects.create(
            projeto=self.projeto,
            freelancer=self.perfil_freelancer,
            preco=1000.00,
            tempo_estimado='5 dias',
            mensagem='Proposta de teste.',
            status=1
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['freelancer'], self.perfil_freelancer.pk)
        self.assertEqual(data[0]['preco'], '1000.00')
        self.assertEqual(data[0]['nome_status'], 'PENDENTE')