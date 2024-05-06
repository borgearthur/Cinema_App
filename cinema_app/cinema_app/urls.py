from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name = 'home'),
    path('cadastro_filme/', views.cadastro_filme, name='cadastro_filme'),
    path('cadastro_alimento/', views.cadastro_alimento, name='cadastro_alimento'),
    path('UserCadastro/',views.UserCadastro, name='UserCadastro'),
    path('detalhes_filme/<int:filme_id>/', views.detalhes_filme, name='detalhes_filme'),
    path('detalhes_alimento/<int:alimento_id>/', views.detalhes_alimento, name='detalhes_alimento'),
    path('favoritos/', views.lista_favoritos, name='favoritos'),
    path('favoritar_filme/<int:filme_id>', views.favoritar_filme, name='favoritar_filme'),
    path('favoritar_alimento/<int:alimento_id>', views.favoritar_alimento, name='favoritar_alimento'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]