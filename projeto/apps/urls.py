from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name = 'home'),
    path('buscar-cafeterias/', views.buscar_cafeterias, name='buscar_cafeterias'),
    path('cadastro_cafeteria/', views.cadastro_cafeteria, name='cadastro_cafeteria'),
    path('cadastro_cafeteria_sucesso/', views.cadastro_cafeteria_sucesso, name='cadastro_cafeteria_sucesso'),
    path('cadastro_user_sucesso/', views.cadastro_user_sucesso, name='cadastro_user_sucesso'),
    path('cafeteria/<int:filme_id>/enviar-email/', enviar_email, name='enviar-email'),
    path('cafeteria/<int:filme_id>/', perfil_cafeteria, name='perfil-cafeteria'),
    path('cafeteria/<int:filme_id>/whatsapp/', enviar_whatsapp, name='enviar_whatsapp'),
    path('cancelar_compra/<int:compra_id>/', cancelar_compra, name='cancelar_compra'),
    path('detalhes/<int:filme_id>/', views.detalhes_anonimo, name='detalhes_anonimo'),
    path('editar_compra/<int:compra_id>/', editar_compra, name='editar_compra'),
    path('excluir_compra/<int:compra_id>/', excluir_compra, name='excluir_compra'),
    path('favoritos/', views.lista_favoritos, name='favoritos'),
    path('favoritar/<int:filme_id>', views.favoritar, name='favoritar'),
    path('historico/', views.lista_historico,name='historico'),
    path('cafeteria/detalhes/<int:filme_id>/', detalhes, name='detalhes'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('minhas_compras/', minhas_compras, name='minhas_compras'),
    path('comprar_filme/<int:filme_id>/', criar_compra, name='criar_compra'),
    path('UserCadastro/',views.UserCadastro, name='UserCadastro'),
    path('cadastro_empresario_sucesso/', views.cadastro_empresario_sucesso, name='cadastro_empresario_sucesso'),
    path('cafeterias_empresarios/', views.cafeterias_empresarios, name='cafeterias_empresarios'),
    path('acesso_negado_cadastrar_cafeteria/', views.acesso_negado_cadastrar_cafeteria, name='acesso_negado_cadastrar_cafeteria'),
    path('avaliar/<int:filme_id>/', views.avaliar_filme, name='avaliar_filme'),
    path('avaliacao_sucesso/', views.avaliacao_sucesso, name='avaliacao_sucesso'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('editar_perfil', editar_perfil, name='editar_perfil'),
    path('editar_perfil_sucesso/', views.editar_perfil_sucesso, name='editar_perfil_sucesso'),
    path('editar_cadastro_cafeteria_sucesso/', views.editar_cadastro_cafeteria_sucesso, name='editar_cadastro_cafeteria_sucesso'),
    path('cafeteria/<int:filme_id>/editar/', editar_cadastro_filme, name='editar_cadastro'),
]