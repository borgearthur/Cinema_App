
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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