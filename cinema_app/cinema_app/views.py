from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def cadastro(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'apps/cadastro.html', {"erro": "Usuário já existe"})
        elif User.objects.filter(email=email).exists():
            return render(request, 'apps/cadastro.html', {"erro": "Email já cadastrado"})

        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
        login(request, user)
        request.session["usuario"] = username
        return redirect(home)
        
    return render(request, 'apps/cadastro.html')

def home(request):
    filmes = Filme.objects.all()
    return render(request, 'app/home_user.html', {'filmes': filmes})

@login_required
def alterar_filmes(request, filme_id):
    try:
        horario = Horario.objects.filter(id=filme_id)
    except Horario.DoesNotExist:
        return HttpResponse("Filme não Encontrado")
    return render(request, 'apps/filme.html', {'horario': horario})

@login_required
def criar_filmes(request):
    filmes = Filme.objects.filter(proprietario_nome=request.user.username)
    return render(request, 'app/filmes.html', {'filmes': filmes})