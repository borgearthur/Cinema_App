from django import urls
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'cinema_app'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('alterar/', views.alterar_filmes, name="alterar"),
    path('criar/', views.criar_filmes, name='criar'), 
    path('criargenero/', views.criar_genero, name='criar-genero'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)