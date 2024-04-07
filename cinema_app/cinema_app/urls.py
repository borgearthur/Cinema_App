from django import urls
from django.urls import path
from . import views


app_name = 'cinema_app'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('cadastro/', views.alterar_filmes, name="cadastro"),
    path('cadastrar_espaco/', views.criar_filmes, name='cadastrar_espaco'),   
]
