from django.db import models
from django.contrib.auth.models import User



    
class Genero(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'user')

class Filme (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=150, null=False, blank=False)
    duracao = models.PositiveIntegerField(null=False, blank=False)
    data_de_lancamento = models.DateTimeField(null=False, blank=False)
    cartaz = models.FileField(upload_to='postee/')
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return self.name

class Alimento (models.Model):
    nome = models.CharField(max_length=200, null=False)
    preco = models.FloatField()
    cartaz = models.FileField(upload_to='comida/')

    def __str__(self):
        return self.name

class Review(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
   text = models.TextField(max_length=10000, default="minha Review legal!")