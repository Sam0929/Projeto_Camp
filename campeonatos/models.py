from django.db import models

class Campeonato(models.Model):
    nome = models.CharField(max_length=100)
    data_inicio = models.DateTimeField()  # Alterado para DateTimeField
    data_fim = models.DateTimeField()  # Alterado para DateTimeField
    descricao = models.TextField()
    participantes = models.ManyToManyField('Participante', related_name='campeonatos')
    premiação = models.DecimalField(max_digits=10, decimal_places=2)
    numero_maximo_participantes = models.PositiveIntegerField(default=10)  
    
    def __str__(self):
        return self.nome

class Participante(models.Model):
    nome_participante = models.CharField(max_length=100)
    email_participante = models.EmailField()
    equipe_participante = models.CharField(max_length=100)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='participante_set')  # Alteração aqui
    

    
    def __str__(self):
        return self.nome_participante  # Corrija para usar o nome correto do campo


class Inscricao(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='inscricao_set')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)  # Alterado para referenciar Participante

    def __str__(self):
        return f'{self.participante.nome} - {self.campeonato}'