from django.db import models

class Campeonato(models.Model):
    nome = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    descricao = models.TextField()
    participantes = models.ManyToManyField('Participante', related_name='campeonatos')
    premiação = models.DecimalField(max_digits=10, decimal_places=2)
    numero_maximo_participantes = models.PositiveIntegerField(default=10)  
    
    def __str__(self):
        return self.nome

class Participante(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    equipe = models.CharField(max_length=100)
    

    
    def __str__(self):
        return self.nome


class Inscricao(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='inscricao_set')
    nome_participante = models.CharField(max_length=100)
    email_participante = models.EmailField()
    equipe_participante = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome_participante} - {self.campeonato}'