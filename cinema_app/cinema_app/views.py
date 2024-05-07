from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    filmes = Filme.objects.all()
    alimentos = Alimento.objects.all()
    return render(request, 'home.html', {'filmes': filmes}, {'alimentos': alimentos})

def detalhes_filme(request, filme_id):
    if request.user.is_authenticated:
        filme = get_object_or_404(Filme, id=filme_id)
        usuario = request.user
        favorito = Favorito.objects.filter(usuario=usuario, filme=filme).exists()
        detalhes_filme = filme.detalhes()
        return render(request, 'detalhes_filme.html', {'filme': filme, 'detalhes_filme': detalhes_filme, 'favorito':favorito})
    else:
        filme = get_object_or_404(Filme, id=filme_id)
        detalhes_filme = filme.detalhes()
        return render(request, 'detalhes_filme.html', {'filme': filme, 'detalhes_filme': detalhes_filme})
    

def detalhes_alimento(request, alimento_id):
    if request.user.is_authenticated:
        alimento = get_object_or_404(Alimento, id=alimento_id)
        usuario = request.user
        favorito = Favorito.objects.filter(usuario=usuario, alimento=alimento).exists()
        detalhes_alimento = alimento.detalhes()
        return render(request, 'detalhes_alimento.html', {'alimento': alimento, 'detalhes_alimento': detalhes_alimento, 'favorito':favorito})
    else:
        alimento = get_object_or_404(Alimento, id=alimento_id)
        detalhes_alimento = alimento.detalhes()
        return render(request, 'detalhes_alimento.html', {'alimento': alimento, 'detalhes_alimento': detalhes_alimento})

@login_required
def favoritar_filme(request, filme_id):
    filme = get_object_or_404(Filme, id=filme_id)
    
    if request.method == 'POST' or request.method == 'GET':
        usuario = request.user
        
        favorito_existente = Favorito.objects.filter(usuario=usuario, filme=filme).exists()
        
        if not favorito_existente:
            Favorito.objects.create(usuario=usuario, filme=filme)
        else:
            favorito = Favorito.objects.filter(usuario=usuario, filme=filme).first()
            favorito.delete()       
        return redirect('favoritos')
    
    return redirect('home')

@login_required
def favoritar_alimento(request, alimento_id):
    alimento = get_object_or_404(Filme, id=alimento_id)
    
    if request.method == 'POST' or request.method == 'GET':
        usuario = request.user
        
        favorito_existente = Favorito.objects.filter(usuario=usuario, alimento=alimento).exists()
        
        if not favorito_existente:
            Favorito.objects.create(usuario=usuario, alimento=alimento)
        else:
            favorito = Favorito.objects.filter(usuario=usuario, alimento=alimento).first()
            favorito.delete()       
        return redirect('favoritos')
    
    return redirect('home')

@login_required
def lista_favoritos(request):
    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(usuario=request.user)
        return render(request, 'favoritos.html', {'favoritos': favoritos})
    else:
        return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            username = User.objects.get(email=email).username
        except ObjectDoesNotExist:
            return render(request, 'login.html', {'error': 'Usuário não encontrado'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

def logout(request):
    logout(request)
    if "usuario" in request.session:
        del request.session["usuario"]
    return redirect(home)

def cadastro_filme(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            return render(request, 'cadastro_filme.html', {'form': request.POST})

        if User.objects.filter(email=email).exists():
            return render(request, 'cadastro_filme.html', {'form': request.POST})

        senha_criptografada = make_password(senha)
        username = request.POST.get('username')
        nome_filme = request.POST.get('nome_filme')
        descricao = request.POST.get('descricao')
        duracao = request.POST.get('duracao')

        filme = Filme(
            username=username,
            nome_filme=nome_filme,
            descricao=descricao,
            email=email,
            duracao=duracao,
            senha=senha_criptografada,
        )

        if 'foto_filme' in request.FILES:
            filme.cartaz = request.FILES['foto_filme']

        try:
            filme.full_clean()
            filme.save()
        except ValidationError:
            return render(request, 'cadastro_filme.html', {'form': request.POST})

        user = User.objects.create_user(password=senha, email=email, first_name=username)
        login(request, user)
        request.session["usuario"] = email 

        return redirect('home') 

    return render(request, 'cadastro_filme.html')

def cadastro_alimento(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            return render(request, 'cadastro_alimento.html', {'form': request.POST})

        if User.objects.filter(email=email).exists():
            return render(request, 'cadastro_alimento.html', {'form': request.POST})

        senha_criptografada = make_password(senha)
        username = request.POST.get('username')
        nome_alimento = request.POST.get('nome_alimento')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')

        alimento = Alimento(
            username=username,
            nome_alimento=nome_alimento,
            descricao=descricao,
            email=email,
            preco=preco,
            senha=senha_criptografada,
        )

        if 'foto_comida' in request.FILES:
            alimento.cartaz = request.FILES['foto_comida']

        try:
            alimento.full_clean()
            alimento.save()
        except ValidationError:
            return render(request, 'cadastro_alimento.html', {'form': request.POST})

        user = User.objects.create_user(password=senha, email=email, first_name=username)
        login(request, user)
        request.session["usuario"] = email 

        return redirect('home') 

    return render(request, 'cadastro_alimento.html')

def UserCadastro(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
                return render(request, 'cadastro_usuario.html', {'form': request.POST})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro_usuario.html', {"erro": "Usuário já existe"})
        if User.objects.filter(email=email).exists():
            return render(request, 'cadastro_usuario.html', {"erro": "Email já cadastrado"})

        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
        login(request, user)
        request.session["usuario"] = email
        return redirect('cadastro_user_sucesso')
        
    return render(request, 'cadastro_usuario.html')