from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import Filme, Avaliacao, UserCliente
from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth import logout as auth_logout
from django.utils import timezone
from django.db.models import Max
import json
from django.core.files.storage import FileSystemStorage
import random

def home(request):
    filmes = Filme.objects.all()
    return render(request, 'home.html', {'filmes': filmes})

def buscar_cafeterias(request):
    if 'termo' in request.GET:
        termo = request.GET['termo']
        resultados = Filme.objects.filter(Q(nome_cafeteria__icontains=termo) | Q(descricao__icontains=termo))
        if resultados:
            return render(request, 'resultado_busca.html', {'resultados': resultados, 'termo': termo})
        else:
            mensagem_alerta = f'Nenhuma cafeteria encontrada com o termo "{termo}".'
            return render(request, 'resultado_busca.html', {'mensagem_alerta': mensagem_alerta})
    else:
        return redirect('home')

@login_required
def cadastro_cafeteria(request):
    usuario = request.user
    email = usuario.email

    print(f"Conteúdo da sessão: {request.session.items()}")
    print(f"Usuário logado: {usuario.username}, ID: {usuario.id}")
    print(f"Grupos do usuário: {[group.name for group in usuario.groups.all()]}")

    is_empresario = usuario.groups.filter(name='Empresários').exists()
    print(f"Usuário é empresário: {is_empresario}")

    if not is_empresario:
        print("Usuário não está no grupo 'Empresários'.")
        messages.error(request, 'Apenas empresários podem cadastrar cafeterias.')
        return redirect('acesso_negado_cadastrar_cafeteria')

    try:
        user_cliente = UserCliente.objects.get(user=usuario)
        print(f"UserCliente encontrado: {user_cliente}")
    except UserCliente.DoesNotExist:
        print("UserCliente não encontrado.")
        messages.error(request, 'Perfil de usuário não encontrado. Complete seu cadastro.')
        return redirect('cadastro_usuario')

    print(f"user_cliente.is_business: {user_cliente.is_business}")

    if request.method == 'POST':
        responsavel = request.POST.get('responsavel')
        nome_cafeteria = request.POST.get('nome_cafeteria')
        endereco = request.POST.get('endereco')
        descricao = request.POST.get('descricao')
        whatsapp = request.POST.get('whatsapp')
        horas_funcionamento = request.POST.get('horas_funcionamento')
        link_redesocial = request.POST.get('link_redesocial', '')
        cnpj = request.POST.get('cnpj')
        site_cafeteria = request.POST.get('site_cafeteria')
        foto_ambiente = request.POST.get('foto_ambiente')

        if not whatsapp.isdigit() or len(whatsapp) != 13:
            return render(request, 'cadastro_cafeteria.html', {"erro": "O número de WhatsApp deve ter 13 dígitos."})

        if not cnpj.isdigit() or len(cnpj) != 14:
            return render(request, 'cadastro_cafeteria.html', {"erro": "O CNPJ deve conter apenas números e ter 14 dígitos."})

        if Filme.objects.filter(whatsapp=whatsapp).exists():
            return render(request, 'cadastro_cafeteria.html', {"erro": "O número de WhatsApp já está em uso."})

        if Filme.objects.filter(cnpj=cnpj).exists():
            return render(request, 'cadastro_cafeteria.html', {"erro": "O CNPJ já está em uso."})
        
        if foto_ambiente in request.FILES:
            Filme.foto_ambiente = request.FILES['foto_ambiente']

        filme = filme(
            responsavel=responsavel,
            nome_cafeteria=nome_cafeteria,
            endereco=endereco,
            descricao=descricao,
            email=email,
            whatsapp=whatsapp,
            horas_funcionamento=horas_funcionamento,
            link_redesocial=link_redesocial,
            cnpj=cnpj,
            site_cafeteria=site_cafeteria,
            empresario=user_cliente
        )

        if 'foto_ambiente' in request.FILES:
            Filme.foto_ambiente = request.FILES['foto_ambiente']

        Filme.full_clean()
        Filme.save()
        return redirect('cadastro_cafeteria_sucesso')

    return render(request, 'cadastro_cafeteria.html')

def cadastro_cafeteria_sucesso(request):
    return render(request, 'cadastro_cafeteria_sucesso.html')

def cadastro_user_sucesso(request):
    return render(request, 'cadastro_user_sucesso.html')

@login_required
def cancelar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, cliente__email=request.user.email)

    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'Compra cancelada com sucesso.')
        return redirect('minhas_compras')
    
    return render(request, 'apps/cancelar_reserva.html', {'compra': compra})

@login_required
def criar_compra(request, filme_id):
    filme = get_object_or_404(Filme, id=filme_id)
    cliente = get_object_or_404(UserCliente, email=request.user.email)
    
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        data_compra = request.POST.get('data_compra')
        horario_compra = request.POST.get('horario_compra')
        numero_de_pessoas = int(request.POST.get('numero_de_pessoas', 1))
        observacao = request.POST.get('observacao', '')

        if not nome_cliente or not data_compra or not horario_compra:
            return render(request, 'comprar_Filme.html', {
                'filme': filme,
                'error_message': 'Por favor, preencha todos os campos obrigatórios.'
            })

        try:
            data_compra = datetime.strptime(data_compra, '%Y-%m-%d').date()
            horario_compra = datetime.strptime(horario_compra, '%H:%M').time()
        except ValueError:
            return render(request, 'comprar_Filme.html', {
                'filme': filme,
                'error_message': 'Formato de data ou horário inválido.'
            })

        today_date = datetime.today().date()
        if data_compra < today_date:
            return render(request, 'comprar_Filme.html', {
                'filme': filme,
                'error_message': 'A data selecionada deve ser futura.'
            })

        if numero_de_pessoas <= 0:
            return render(request, 'comprar_Filme.html', {
                'filme': filme,
                'error_message': 'O número de pessoas deve ser maior que zero.'
            })

        compras_conflitantes = compraFilme.objects.filter(
            filme=filme,
            data_compra=data_compra,
            horario_compra=horario_compra
        )

        if compras_conflitantes.exists():
            return render(request, 'comprar_Filme.html', {
                'filme': filme,
                'error_message': 'Café já comprado para o horário solicitado!'
            })

        compra = comprafilme(
            filme=filme,
            cliente=cliente,
            data_compra=data_compra,
            horario_compra=horario_compra,
            numero_de_pessoas=numero_de_pessoas,
            observacao=observacao
        )
        compra.save()
        
        messages.success(request, 'compra efetuada com sucesso.')
        return redirect('minhas_compras')
    
    else:
        compras = compraFilme.objects.filter(filme=filme).values('data_compra', 'horario_compra')
        horarios_comprados = {}
        for compra in compras:
            data_str = compra['data_compra'].strftime('%Y-%m-%d')
            horario_str = compra['horario_compra'].strftime('%H:%M')
            if data_str not in horarios_comprados:
                horarios_comprados[data_str] = []
            horarios_comprados[data_str].append(horario_str)

        return render(request, 'comprar_Filme.html', {
            'filme': filme,
            'horarios_comprados_json': json.dumps(horarios_comprados)
    })

def detalhes_anonimo(request, filme_id):
        filme = get_object_or_404(filme, id=filme_id)
        detalhes_filme = Filme.detalhes()

        outras_cafeterias = list(Filme.objects.exclude(id=filme_id))
        random.shuffle(outras_cafeterias)
        outras_cafeterias = outras_cafeterias[:4]

        return render(request, 'detalhes.html', {'filme': filme, 'detalhes_filme': detalhes_filme, 'outras_cafeterias': outras_cafeterias})

@login_required
def editar_compra(request, compra_id):
    compra = get_object_or_404(comprafilme, id=compra_id)
    filme = compra.filme
    
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        data_compra = request.POST.get('data_compra')
        horario_compra = request.POST.get('horario_compra')
        numero_de_pessoas = int(request.POST.get('numero_de_pessoas', 1))
        observacao = request.POST.get('observacao', '')

        if not nome_cliente or not data_compra or not horario_compra:
            return render(request, 'editar_reserva.html', {
                'compra': compra,  'filme':filme,
                'error_message': 'Por favor, preencha todos os campos obrigatórios.'
            })

        try:
            data_compra = datetime.strptime(data_compra, '%Y-%m-%d').date()
            horario_compra = datetime.strptime(horario_compra, '%H:%M').time()
        except ValueError:
            return render(request, 'editar_reserva.html', {
                'compra': compra, 'filme':filme,
                'error_message': 'Formato de data ou horário inválido.'
            })

        today_date = datetime.today().date()
        if data_compra < today_date:
            return render(request, 'editar_reserva.html', {
                'compra': compra, 'filme':filme,
                'error_message': 'A data selecionada deve ser futura.'
            })

        if numero_de_pessoas <= 0:
            return render(request, 'editar_reserva.html', {
                'compra': compra, 'filme':filme,
                'error_message': 'O número de pessoas deve ser maior que zero.'
            })

        compras_conflitantes = compraFilme.objects.filter(
            filme=filme,
            data_compra=data_compra,
            horario_compra=horario_compra
        ).exclude(id=compra.id)

        if compras_conflitantes.exists():
            return render(request, 'editar_reserva.html', {
                'compra': compra, 'filme':filme,
                'error_message': 'Café já comprado para o horário solicitado!'
            })

        compra.data_compra = data_compra
        compra.horario_compra = horario_compra
        compra.numero_de_pessoas = numero_de_pessoas
        compra.observacao = observacao
        compra.save()
        
        messages.success(request, 'compra atualizada com sucesso.')
        return redirect('minhas_compras')
    
    return render(request, 'editar_reserva.html', {
        'compra': compra, 'filme':filme
    })

@login_required
def enviar_whatsapp(request, filme_id):
    cafeteria = get_object_or_404(filme, pk=filme_id)
    if cafeteria.whatsapp:
        whatsapp_url = f"https://wa.me/{cafeteria.whatsapp}"
        return redirect(whatsapp_url)
    else:
        messages.error(request, "Número de WhatsApp não disponível.")
        return HttpResponseRedirect(reverse('perfil_cafeteria', args=[filme_id]))

def enviar_email(request, filme_id):
    cafeteria = get_object_or_404(filme, pk=filme_id)
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem', '')
        send_mail(
            'Mensagem do MyfilmeApp',
            mensagem,
            'from@example.com',
            [cafeteria.email],
            fail_silently=False,
        )
        messages.success(request, "Email enviado com sucesso!")
        return render(request, 'email_enviado.html', {'cafeteria': cafeteria})
    return render(request, 'enviar_email.html', {'cafeteria': cafeteria})

@login_required
def excluir_compra(request, compra_id):
    compra = get_object_or_404(comprafilme, id=compra_id)
    
    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'compra excluída com sucesso.')
        return redirect('minhas_compras')
    
    return render(request, 'excluir_reserva.html', {
        'compra': compra
    })

@login_required
def favoritar(request, filme_id):
    filme = get_object_or_404(filme, id=filme_id)
    
    if request.method == 'POST' or request.method == 'GET':
        usuario = request.user
        
        favorito_existente = Favorito.objects.filter(usuario=usuario, filme=filme).exists()
        
        if not favorito_existente:
            Favorito.objects.create(usuario=usuario, filme=filme)
            messages.success(request, 'cafeteria favoritada com sucesso!')
        else:
            favorito = Favorito.objects.filter(usuario=usuario, filme=filme).first()
            favorito.delete()  # Remove o favorito se existir
            messages.success(request, 'cafeteria removida dos favoritos.')
        
        return redirect('favoritos')
    
    return redirect('home')


@login_required
def lista_favoritos(request):
    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(usuario=request.user)
        return render(request, 'favoritos.html', {'favoritos': favoritos})
    else:
        return redirect('login')
    
@login_required
def registrar_historico(request, filme_id): 
    filme = get_object_or_404(filme, id=filme_id)
    
    usuario = request.user
    # Evita múltiplas entradas no mesmo dia
    visita_hoje = Historico.objects.filter(usuario=usuario, filme=filme, visited_at__date=timezone.now().date()).exists()
    
    if not visita_hoje:
        Historico.objects.create(usuario=usuario, filme=filme)

    return redirect('filme_detalhes', filme_id=Filme.id)

@login_required
def lista_historico(request):
    if request.user.is_authenticated:
        historico = Historico.objects.filter(usuario=request.user).order_by('-visited_at')
        return render(request, 'historico.html', {'historico': historico})
    else:
        return redirect('login')
    
@login_required
def detalhes(request, filme_id):
    filme = get_object_or_404(filme, id=filme_id)
    range_5 = range(1, 6)
    usuario = request.user
    favorito = Favorito.objects.filter(usuario=usuario, filme=filme).exists()
    detalhes_filme = Filme.detalhes()

    outras_cafeterias = list(Filme.objects.exclude(id=filme_id))
    random.shuffle(outras_cafeterias)
    outras_cafeterias = outras_cafeterias[:4]


    today = timezone.localdate()

    visita_hoje = Historico.objects.filter(
        usuario=usuario, 
        filme=filme, 
        visited_at__date=today,
    ).exists()

    if not visita_hoje:
        Historico.objects.create(usuario=usuario, filme=filme, visited_at=timezone.now())

    star_range = range(1, 6)

    return render(request, 'detalhes.html', {
        'filme': filme,
        'detalhes_filme': detalhes_filme,
        'favorito': favorito,
        'star_range': star_range,
        'range_5': range_5,
        'outras_cafeterias': outras_cafeterias
    })
    
def limpar_historico_duplicado():
    # Encontrar a última visita para cada usuário e cafeteria por dia
    ultimas_visitas = Historico.objects.values('usuario_id', 'filme_id', 'visited_at__date').annotate(
        ultima_visita=Max('visited_at')
    )

    # Converter resultados em uma lista de IDs de visitas para manter
    ids_para_manter = [visita['ultima_visita'] for visita in ultimas_visitas]

    # Excluir todas as visitas que não estão na lista de IDs para manter
    Historico.objects.exclude(id__in=ids_para_manter).delete()

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
            if user.groups.filter(name='Empresários').exists():
                return redirect('home')
            else: 
                return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
        
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    if "usuario" in request.session:
        del request.session["usuario"]
    request.session.flush()
    return redirect('home')

@login_required
def minhas_compras(request):
    try:
        cliente = UserCliente.objects.get(email=request.user.email)
    except UserCliente.DoesNotExist:
        return redirect('login')

    compras = compraFilme.objects.filter(cliente=cliente)
    return render(request, 'minhas_compras.html', {'compras': compras})

def perfil_cafeteria(request, filme_id):
    cafeteria = get_object_or_404(filme, pk=filme_id)
    return render(request, 'perfil_cafeteria.html', {'cafeteria': cafeteria})

def UserCadastro(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')
        is_business = request.POST.get('is_business') == 'on'

        if password != confirm_password:
                messages.error(request, 'As senhas não correspondem.')
                return render(request, 'cadastro_usuario.html', {'form': request.POST})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro_usuario.html', {"erro": "Usuário já existe"})
        if User.objects.filter(email=email).exists():
            return render(request, 'cadastro_usuario.html', {"erro": "Email já cadastrado"})

        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)

        if is_business:
            empresario_group = Group.objects.get(name='Empresários')
            user.groups.add(empresario_group)

        user_cliente = UserCliente(user=user, nome_completo=name, email=email, is_business=is_business)
        user_cliente.save()

        login(request, user)
        request.session["usuario"] = email

        print(f"Usuário {username} criado com is_business={is_business}")

        if is_business:
            return redirect('cadastro_empresario_sucesso') 
        else:
            return redirect('cadastro_user_sucesso')
        
    return render(request, 'cadastro_usuario.html')

@login_required
def cadastro_empresario_sucesso(request):
    return render(request, 'cadastro_empresario_sucesso.html')

@login_required
def cafeterias_empresarios(request):
    usuario = request.user
    empresaario = usuario.usercliente
    cafeterias = Filme.objects.filter(empresario=empresaario)
    return render(request, 'cafeterias_empresarios.html', {'cafeterias': cafeterias})

def acesso_negado_cadastrar_cafeteria(request):
    return render(request, 'acesso_negado_cadastrar_cafeteria.html')

@login_required
def avaliar_filme(request, filme_id):
    filme = get_object_or_404(filme, id=filme_id)
    try:
        cliente = get_object_or_404(UserCliente, user=request.user)
    except UserCliente.DoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado. Complete seu cadastro.')
        return redirect('cadastro_usuario')

    if request.method == 'POST':
        avaliacao = request.POST.get('avaliacao')
        comentario = request.POST.get('comentario')
        valor_gasto = request.POST.get('valor_gasto')
        foto_experiencia = request.FILES.get('foto_experiencia')

        if not avaliacao or not comentario or not valor_gasto:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return render(request, 'avaliar_Filme.html', {'filme': filme, 'range': range(1, 6)})

        Avaliacao.objects.create(
            filme=filme,
            cliente=cliente,
            avaliacao=int(avaliacao),
            comentario=comentario,
            valor_gasto=valor_gasto,
            foto_avaliacao=foto_experiencia
        )

        messages.success(request, 'Avaliação enviada com sucesso.')
        return redirect('avaliacao_sucesso')

    return render(request, 'avaliar_Filme.html', {'filme': filme, 'range': range(1, 6)})

@login_required
def avaliacao_sucesso(request):
    return render(request, 'avaliacao_sucesso.html')

@login_required
def perfil_usuario(request):
    user_cliente = UserCliente.objects.get(user=request.user)
    print(f"Tipo de Usuário: {user_cliente.is_business}")
    context = {
        'user_cliente': user_cliente
    }
    return render(request, 'perfil_usuario.html', context)

@login_required
def editar_perfil(request):
    user_cliente = UserCliente.objects.get(user=request.user)
    if request.method == 'POST':
        username = request.POST.get('username')
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')

        if not username:
            username = user_cliente.user.username
        if not nome_completo:
            nome_completo = user_cliente.nome_completo
        if not email:
            email = user_cliente.email

        if UserCliente.objects.filter(email=email).exclude(id=user_cliente.id).exists():
            return render(request, 'editar_perfil.html', {
                'error': 'Este email já está em uso por outro usuário.',
                'user_cliente': user_cliente
            })

        if User.objects.filter(username=username).exclude(id=user_cliente.user.id).exists():
            return render(request, 'editar_perfil.html', {
                'error': 'Este username já está em uso por outro usuário.',
                'user_cliente': user_cliente
            })

        user_cliente.user.username = username
        user_cliente.nome_completo = nome_completo
        user_cliente.email = email

        if profile_image:
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            user_cliente.profile_image = filename
            
        user_cliente.save()

        return redirect('editar_perfil_sucesso')
    else:
        return render(request, 'editar_perfil.html', {'user_cliente': user_cliente})

def editar_perfil_sucesso(request):
    return render(request, 'editar_perfil_sucesso.html')

def editar_cadastro_filme(request, filme_id):
    # Obter o UserCliente associado ao usuário logado
    user_cliente = request.user.usercliente
    
    # Obter a cafeteria específica associada ao UserCliente
    filme = get_object_or_404(filme, id=filme_id, empresario=user_cliente)
    
    if request.method == 'POST':
        responsavel = request.POST.get('responsavel') or Filme.responsavel
        nome_cafeteria = request.POST.get('nome_cafeteria') or Filme.nome_cafeteria
        endereco = request.POST.get('endereco') or Filme.endereco
        descricao = request.POST.get('descricao') or Filme.descricao
        email = request.POST.get('email') or Filme.email
        whatsapp = request.POST.get('whatsapp') or Filme.whatsapp
        horas_funcionamento = request.POST.get('horas_funcionamento') or Filme.horas_funcionamento
        link_redesocial = request.POST.get('link_redesocial') or Filme.link_redesocial
        foto_ambiente = request.FILES.get('foto_ambiente') or Filme.foto_ambiente
        cnpj = request.POST.get('cnpj') or Filme.cnpj
        site_cafeteria = request.POST.get('site_cafeteria') or Filme.site_cafeteria

        if not whatsapp.isdigit() or len(whatsapp) != 13:
            return render(request, 'editar_cadastro_Filme.html', {
                'erro': 'O número de WhatsApp deve conter apenas números e ter 13 dígitos.',
                'filme': filme
            })

        if not cnpj.isdigit() or len(cnpj) != 14:
            return render(request, 'editar_cadastro_Filme.htmll', {
                'erro': 'O CNPJ deve conter apenas números e ter 14 dígitos.',
                'filme': filme
            })
        
        if Filme.objects.filter(cnpj=cnpj).exclude(pk=Filme.pk).exists():
            return render(request, 'editar_cadastro_Filme.html', {
                'erro': 'Este CNPJ já está em uso por outra cafeteria.',
                'filme': filme
            })
        
        if Filme.objects.filter(whatsapp=whatsapp).exclude(pk=Filme.pk).exists():
            return render(request, 'editar_cadastro_Filme.html', {
                'erro': 'Este Whatsapp já está em uso por outra cafeteria.',
                'filme': filme
            })

        Filme.responsavel = responsavel
        Filme.nome_cafeteria = nome_cafeteria
        Filme.endereco = endereco
        Filme.descricao = descricao
        Filme.email = email
        Filme.whatsapp = whatsapp
        Filme.horas_funcionamento = horas_funcionamento
        Filme.link_redesocial = link_redesocial
        Filme.foto_ambiente = foto_ambiente
        Filme.cnpj = cnpj
        Filme.site_cafeteria = site_cafeteria
        
        Filme.save()

        return redirect('editar_cadastro_cafeteria_sucesso')
    
    return render(request, 'editar_cadastro_Filme.html', {
        'filme': filme
    })

def editar_cadastro_cafeteria_sucesso(request):
    return render(request, 'editar_cadastro_cafeteria_sucesso.html')

