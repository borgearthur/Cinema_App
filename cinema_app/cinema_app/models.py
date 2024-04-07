from django.db import models

class Filme (models.Model):
    
    nome = models.CharField(max_length=200, null=False)
    duração = models.DurationField()
    data_de_lançamento = models.DateField()
    cartaz = models.ImageField(upload_to='poster/')

    class Meta:
        app_label = 'cinema_app'
        verbose_name_plural = 'Filmes'

class Horario(models.Model):
    peso = models.FloatField(max_length=4, null=False)
    altura = models.FloatField(max_length = 4, null=False)
    restricao_alimentar = models.TextField(max_length = 100)
    tdah = models.CharField(max_length = 4)
    pcd = models.CharField(max_length = 4)

    class Meta:
        app_label = 'cinema_app'
        verbose_name_plural = 'Horarios'