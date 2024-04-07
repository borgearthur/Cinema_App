from django.contrib import admin
from django.urls import path

app_name = 'cinema_app'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('cadastrar_espaco/', views.cadastrar_espaco, name='cadastrar_espaco'),
    path('detalhes/<int:espaco_id>/', views.detalhes, name='detalhes'),
    
]
