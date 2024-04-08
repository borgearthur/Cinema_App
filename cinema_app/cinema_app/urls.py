from django import urls
from django.urls import path
from . import views


app_name = 'cinema_app'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('alterar/', views.alterar_filmes, name="alterar"),
    path('criar/', views.criar_filmes, name='criar'),   
]
