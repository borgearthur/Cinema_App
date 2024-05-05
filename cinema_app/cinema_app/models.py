from django.db import models
from django.contrib.auth.models import User



class Filme (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=150, null=False, blank=False)
    duracao = models.PositiveIntegerField(null=False, blank=False)
    data_de_lancamento = models.DateTimeField(null=False, blank=False)
    cartaz = models.FileField(upload_to='poster/')
    nome = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.nome
    def get_short_description(self):
        if len(self.descricao) > 100:
            return self.descricao[:100].__add__("...")
        else:
            return self.descricao


class Alimento (models.Model):
    nome = models.CharField(max_length=200, null=False)
    preco = models.FloatField(null=False, blank=False)
    foto_comida = models.FileField(upload_to='comida/', null=False, blank=False)

    def __str__(self):
        return self.nome

class Review(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
   text = models.TextField(max_length=10000, default="minha Review legal!")

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)

    def _str_(self):
        return f'{self.usuario.username} - {self.filme.nome}'
    
