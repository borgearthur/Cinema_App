
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
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

@login_required
def cadastrar_espaco(request):
    if request.method == 'POST':
        proprietario_nome = request.POST['proprietario_nome']
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        preco_por_noite = request.POST['preco_por_noite']
        endereco = request.POST['endereco']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        pais = request.POST['pais']
        numero_de_quartos = request.POST['numero_de_quartos']
        numero_de_banheiros = request.POST['numero_de_banheiros']
        numero_de_hospedes = request.POST['numero_de_hospedes']
        foto_principal = request.FILES.get('foto_principal', None)

        novo_espaco = Espaco(
            proprietario_nome=proprietario_nome,
            nome=nome,
            descricao=descricao,
            preco_por_noite=preco_por_noite,
            endereco=endereco,
            cidade=cidade,
            estado=estado,
            pais=pais,
            numero_de_quartos=numero_de_quartos,
            numero_de_banheiros=numero_de_banheiros,
            numero_de_hospedes=numero_de_hospedes,
            foto_principal=foto_principal
        )
        novo_espaco.save()

        return redirect('detalhes_espaco', espaco_id=novo_espaco.id)
    else:
        return render(request, 'apps/cadastrar_espaco.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session["usuario"] = username
            return redirect(home)
        else:
            return render(request, 'apps/login.html', {"erro": "Usuário não encontrado"})
    return render(request, 'apps/login.html')

def logout(request):
    logout(request)
    if "usuario" in request.session:
        del request.session["usuario"]
    return redirect(home)

@login_required
def meus_espacos(request):
    espacos = Espaco.objects.filter(proprietario_nome=request.user.username)
    return render(request, 'apps/meus_espacos.html', {'espacos': espacos})

@login_required
def minhas_reservas(request):
    reservas = Reserva.objects.filter(proprietario_nome=request.user.username)
    return render(request, 'apps/minhas_reservas.html', {'reservas': reservas})

def selecionar_espaco_para_reserva(request):
    espacos = Espaco.objects.all()
    return render(request, 'selecionar_espaco_para_reserva.html', {'espacos': espacos})