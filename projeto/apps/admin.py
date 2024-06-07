from django.contrib import admin
from .models import UserCliente, Filme, Favorito, Historico, Compra, Avaliacao

# Função para registrar um modelo se não estiver registrado
def register_model(admin_site, model):
    if model not in admin_site._registry:
        admin_site.register(model)
    else:
        print(f"O modelo {model.__name__} já está registrado.")

# Registrando os modelos
register_model(admin.site, UserCliente)
register_model(admin.site, Filme)
register_model(admin.site, Favorito)
register_model(admin.site, Historico)
register_model(admin.site, Compra)
register_model(admin.site, Avaliacao)