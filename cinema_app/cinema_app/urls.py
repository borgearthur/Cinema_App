from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'cinema_app'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('search/', views.Search.as_view(), name='search'),
    path('filme/<int:id>', views.ViewFilme.as_view(), name='filme'),
    path('review/<int:id>/', views.ReviewView.as_view(), name='review'),
    path('criar/', views.criar_filme, name='criar'), 
    path('criargenero/', views.create_category, name='criar-genero'),
    path('filmes/',views.filmes, name = 'filmes')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
