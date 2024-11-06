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
    gols_time_casa = models.PositiveIntegerField(null=True, blank=True)  # Permitir nulos
    gols_time_fora = models.PositiveIntegerField(null=True, blank=True)  # Permitir nulos

    def __str__(self):
        return f'Resultado: {self.gols_time_casa or "N/A"} - {self.gols_time_fora or "N/A"} ({self.jogo.time_casa.nome} vs {self.jogo.time_fora.nome})'

class RodadasClassificatorias(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='rodadas_classificatorias')
    fase = models.CharField(max_length=50)  # Exemplo: "Oitavas", "Quartas", "Semi", "Final"
    data = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.fase} - {self.campeonato.nome}'

class RodadaEliminatoria(models.Model):
    FASE_CHOICES = [
        ('oitavas', 'Oitavas de Final'),
        ('quartas', 'Quartas de Final'),
        ('semi', 'Semifinais'),
        ('final', 'Final'),
    ]

    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='eliminatorias')
    fase = models.CharField(max_length=50, choices=FASE_CHOICES)  # Incluindo choices para permitir display legível
    data = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.get_fase_display()} - {self.campeonato.nome}'

class JogoEliminatorio(models.Model):
    rodada = models.ForeignKey(RodadaEliminatoria, on_delete=models.CASCADE, related_name='jogos')
    time_casa = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='eliminatorias_como_casa')
    time_fora = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='eliminatorias_como_fora')
    data_horario = models.DateTimeField(null=True, blank=True)
    resultado = models.CharField(max_length=50, blank=True, null=True)  # Exemplo: "2-1"

    def __str__(self):
        return f'{self.time_casa.nome} vs {self.time_fora.nome} - {self.rodada.fase}'
