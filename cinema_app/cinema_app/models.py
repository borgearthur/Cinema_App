from django.db import models
from django.contrib.auth.models import User



class Filme (models.Model):
    username = models.CharField(max_length=100, blank=False, default='Username não informado')
    nome_filme = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True,default="default@example.com")
    duracao = models.PositiveIntegerField(null=False, blank=False)
    descricao = models.TextField(blank=False, default='Descrição não informada')
    foto_filme = models.FileField(upload_to='poster/')
    senha = models.CharField(max_length=128, default='0000')
    def __str__(self):
        return self.nome_filme
    
    def detalhes(self):
        return {
            'username': self.username,
            'nome_filme': self.nome_filme,
            'descricao': self.descricao,
            'email': self.email,
            'duracao': self.duracao,
            'foto_filme': self.foto_filme,
            'senha': self.senha,
        }

    def get_short_description(self):
        if len(self.descricao) > 100:
            return self.descricao[:100].__add__("...")
        else:
            return self.descricao


class Alimento (models.Model):
    username = models.CharField(max_length=100, blank=False, default='Username não informado')
    email = models.EmailField(unique=True,default="default@example.com")
    nome_alimento = models.CharField(max_length=200, null=False)
    preco = models.FloatField(null=False, blank=False)
    descricao = models.TextField(blank=False, default='Descrição não informada')
    foto_alimento = models.FileField(upload_to='comida/', null=False, blank=False)
    senha = models.CharField(max_length=128, default='0000')

    def detalhes(self):
        return {
            'username': self.username,
            'nome_alimento': self.nome_alimento,
            'descricao': self.descricao,
            'email': self.email,
            'preco': self.preco,
            'foto_alimento': self.foto_alimento,
            'senha': self.senha,
        }

    def __str__(self):
        return self.nome_alimento
    
    def get_short_description(self):
        if len(self.descricao) > 100:
            return self.descricao[:100].__add__("...")
        else:
            return self.descricao

class Review(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
   text = models.TextField(max_length=10000, default="minha Review legal!")

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)

    def _str_(self):
        return f'{self.usuario.username} - {self.filme.nome}'
    
