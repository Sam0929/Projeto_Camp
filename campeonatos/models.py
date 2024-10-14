from django.db import models

class Campeonato(models.Model):
    nome = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    descricao = models.TextField()
    participantes = models.ManyToManyField('Participante', related_name='campeonatos')
    premiação = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.nome

class Participante(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    equipe = models.CharField(max_length=100)
    

    
    def __str__(self):
        return self.nome


