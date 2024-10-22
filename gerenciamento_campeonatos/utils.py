from datetime import timedelta
import random
from .models import Rodada, Jogo
from campeonatos.models import Inscricao


def gerar_jogos(campeonato, numero_rodadas, intervalo_dias):
    # Resgata todas as inscrições e agrupa os participantes por times
    inscricoes = Inscricao.objects.filter(campeonato=campeonato)
    times = {}

    # Agrupar participantes por times
    for inscricao in inscricoes:
        equipe = inscricao.participante.equipe_participante
        if equipe not in times:
            times[equipe] = []
        times[equipe].append(inscricao.participante)

    equipes = list(times.keys())
    numero_equipes = len(equipes)

    if numero_equipes < 2:
        return "Não há equipes suficientes para gerar jogos."

    # Adicionar uma equipe fantasma caso o número de equipes seja ímpar
    if numero_equipes % 2 != 0:
        equipes.append(None)  # 'None' representará a equipe que "descansa"

    numero_equipes = len(equipes)
    combinacoes_rodadas = []

    # Round-robin para gerar todas as rodadas
    for rodada_numero in range(numero_rodadas):
        rodada_atual = []
        equipes_disponiveis = equipes[:]

        # Embaralhar para garantir a aleatoriedade nas rodadas
        random.shuffle(equipes_disponiveis)

        while equipes_disponiveis:
            equipe_casa = equipes_disponiveis.pop(0)
            equipe_fora = equipes_disponiveis.pop(0)

            # Adicionar apenas se não for a equipe fantasma
            if equipe_casa and equipe_fora:
                rodada_atual.append((equipe_casa, equipe_fora))

        combinacoes_rodadas.append(rodada_atual)

    data_inicial = campeonato.data_inicio

    # Criar jogos por rodada
    for rodada_numero, jogos in enumerate(combinacoes_rodadas):
        data_rodada = data_inicial + timedelta(days=rodada_numero * intervalo_dias)

        # Verifica se a data da rodada ultrapassa a data de fim do campeonato
        if data_rodada > campeonato.data_fim:
            return "Não é possível gerar rodadas além da data de fim do campeonato."

        rodada, created = Rodada.objects.get_or_create(
            campeonato=campeonato,
            numero=rodada_numero + 1,
            defaults={'data': data_rodada}
        )

        # Criar os jogos da rodada
        for equipe_casa, equipe_fora in jogos:
            time_casa = times[equipe_casa][0]  # Primeiro participante do time da casa
            time_fora = times[equipe_fora][0]  # Primeiro participante do time visitante

            Jogo.objects.create(
                rodada=rodada,
                time_casa=time_casa,
                time_fora=time_fora,
                data_horario=data_rodada
            )

    return "Jogos gerados com sucesso!"
