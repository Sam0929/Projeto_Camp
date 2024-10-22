import itertools
from datetime import timedelta
from .models import Rodada, Jogo

def gerar_jogos(campeonato):
    participantes = list(campeonato.participantes.all())
    print(f"Participantes: {participantes}")  # Para verificar a lista de participantes no terminal
    numero_participantes = len(participantes)

    if numero_participantes < 2:
        return "Não há participantes suficientes para gerar jogos."

    # Gera todas as combinações de jogos
    combinacoes = list(itertools.combinations(participantes, 2))
    data_inicial = campeonato.data_inicio

    for i, (time_casa, time_fora) in enumerate(combinacoes):
        rodada_numero = i // (numero_participantes // 2) + 1
        data_jogo = data_inicial + timedelta(days=rodada_numero * 7)  # Uma rodada por semana

        # Cria ou recupera a rodada
        rodada, created = Rodada.objects.get_or_create(
            campeonato=campeonato,
            numero=rodada_numero,
            defaults={'data': data_jogo}
        )

        # Cria o jogo na rodada
        Jogo.objects.create(
            rodada=rodada,
            time_casa=time_casa,
            time_fora=time_fora,
            data_horario=data_jogo
        )

    return "Jogos gerados com sucesso!"
