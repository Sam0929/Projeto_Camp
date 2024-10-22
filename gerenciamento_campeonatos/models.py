from django.db import models
from campeonatos.models import Campeonato, Participante  # Importando os modelos da aplicação campeonatos


class Rodada(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='rodadas')
    numero = models.PositiveIntegerField()  # Número da rodada
    data = models.DateTimeField()

    def __str__(self):
        return f'Rodada {self.numero} - {self.campeonato.nome}'


class Jogo(models.Model):
    rodada = models.ForeignKey(Rodada, on_delete=models.CASCADE, related_name='jogos')
    time_casa = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='jogos_como_casa')
    time_fora = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='jogos_como_fora')
    data_horario = models.DateTimeField()
    resultado = models.CharField(max_length=50, blank=True, null=True)  # Exemplo: "2-1"

    def __str__(self):
        return f'{self.time_casa.nome} vs {self.time_fora.nome} - Rodada {self.rodada.numero}'


class Resultado(models.Model):
    jogo = models.OneToOneField(Jogo, on_delete=models.CASCADE, related_name='resultado_jogo')
    gols_time_casa = models.PositiveIntegerField(default=0)
    gols_time_fora = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Resultado: {self.gols_time_casa} - {self.gols_time_fora} ({self.jogo.time_casa.nome} vs {self.jogo.time_fora.nome})'
