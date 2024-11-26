from django.db import models
from campeonatos.models import Campeonato, Participante  # Importando os modelos da aplicação campeonatos
from django.contrib.auth.models import User

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

class Comentario(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name='comentarios_jogo')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.usuario.username} no jogo {self.jogo}'


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
    time_casa = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='eliminatorias_como_casa', null=True, blank=True)
    time_fora = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='eliminatorias_como_fora', null=True, blank=True)
    data_horario = models.DateTimeField(null=True, blank=True)
    resultado = models.CharField(max_length=50, blank=True, null=True)  # Exemplo: "2-1"
    placeholder = models.BooleanField(default=False)  # Novo campo placeholder

    def __str__(self):
        return f'{self.time_casa.nome if self.time_casa else "TBD"} vs {self.time_fora.nome if self.time_fora else "TBD"} - {self.rodada.fase}'

class ComentarioEliminatorio(models.Model):
    jogo = models.ForeignKey(
        JogoEliminatorio, 
        on_delete=models.CASCADE, 
        related_name='comentarioseliminatorios'  # Esse é o related_name que usamos na função de obtenção de comentários
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)


class ResultadoEliminatorio(models.Model):
    jogo = models.OneToOneField('JogoEliminatorio', on_delete=models.CASCADE, related_name='resultado_eliminatorio')
    gols_time_casa = models.PositiveIntegerField(null=True, blank=True)  # Permitir nulos
    gols_time_fora = models.PositiveIntegerField(null=True, blank=True)  # Permitir nulos

    def __str__(self):
        return f'Resultado: {self.gols_time_casa or "N/A"} - {self.gols_time_fora or "N/A"} ({self.jogo.time_casa.nome if self.jogo.time_casa else "TBD"} vs {self.jogo.time_fora.nome if self.jogo.time_fora else "TBD"})'


class Penalidade(models.Model):
    TIPO_PENALIDADE_CHOICES = [
        ('amarelo', 'Cartão Amarelo'),
        ('vermelho', 'Cartão Vermelho'),
        ('expulsao', 'Expulsão'),
        ('outro', 'Outro')
    ]

    ALVO_PENALIDADE_CHOICES = [
        ('participante', 'Por Participante'),
        ('casa', 'Equipe Casa'),
        ('fora', 'Equipe Fora')
    ]

    jogo = models.ForeignKey('Jogo', on_delete=models.CASCADE, related_name='penalidades')
    participante = models.ForeignKey(
        'campeonatos.Participante', 
        on_delete=models.CASCADE, 
        related_name='penalidades', 
        null=True, 
        blank=True
    )
    equipe = models.CharField(max_length=15, choices=ALVO_PENALIDADE_CHOICES, null=True, blank=True)
    tipo_penalidade = models.CharField(max_length=50, choices=TIPO_PENALIDADE_CHOICES, null=True, blank=True)
    motivo = models.TextField(blank=True, null=True)

    def __str__(self):
        alvo = self.participante.nome if self.participante else (self.equipe or "N/A")
        return f'{self.tipo_penalidade or "N/A"} - {alvo} ({self.jogo})'


class PenalidadeEliminatoria(models.Model):
    TIPO_PENALIDADE_CHOICES = [
        ('amarelo', 'Cartão Amarelo'),
        ('vermelho', 'Cartão Vermelho'),
        ('expulsao', 'Expulsão'),
        ('outro', 'Outro'),
        ('participante', 'Por Participante'),
        ('equipe', 'Por Equipe')
    ]

    jogo = models.ForeignKey('JogoEliminatorio', on_delete=models.CASCADE, related_name='penalidades_eliminatorias')
    participante = models.ForeignKey('campeonatos.Participante', on_delete=models.CASCADE, related_name='penalidades_eliminatorias', null=True, blank=True)
    tipo_penalidade = models.CharField(max_length=50, choices=TIPO_PENALIDADE_CHOICES, null=True, blank=True)
    motivo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.tipo_penalidade or "N/A"} - {self.participante.nome if self.participante else "N/A"} ({self.jogo})'
