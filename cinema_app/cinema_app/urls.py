from django import urls
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'cinema_app'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('search/', views.ViewFilme.as_view(), name='search'),
    path('review/<int:id>/', views.ReviewView.as_view(), name='review'),
    path('criar/', views.criar_filme, name='criar'), 
    path('criargenero/', views.create_category, name='criar-genero'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
