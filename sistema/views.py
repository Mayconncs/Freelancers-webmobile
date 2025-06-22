from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/freelancer")
        return render(request, 'autenticacao.html', {'mensagem': ''})

    def post(self, request):
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/freelancer")
            messages.error(request, 'Usuário inativo!')
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
        return render(request, 'autenticacao.html')

class Cadastro(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/freelancer")
        return render(request, 'cadastro.html', {'mensagem': ''})

    def post(self, request):
        usuario = request.POST.get('usuario', None)
        email = request.POST.get('email', None)
        senha = request.POST.get('senha', None)
        confirmar_senha = request.POST.get('confirmar_senha', None)

        if not all([usuario, email, senha, confirmar_senha]):
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'cadastro.html')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem!')
            return render(request, 'cadastro.html')

        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'Usuário já existe!')
            return render(request, 'cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado!')
            return render(request, 'cadastro.html')

        try:
            user = User.objects.create_user(
                username=usuario,
                email=email,
                password=senha
            )
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
            return render(request, 'cadastro.html')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)

class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'token': token.key,
            'papel': user.perfil.papel if hasattr(user, 'perfil') else None
        })

class CadastroAPI(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirmar_senha = request.data.get('confirmar_senha')

        if not all([username, email, password, confirmar_senha]):
            return Response({'detail': 'Todos os campos são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirmar_senha:
            return Response({'detail': 'As senhas não coincidem.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Usuário já existe.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Email já cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': f'Erro ao cadastrar: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)