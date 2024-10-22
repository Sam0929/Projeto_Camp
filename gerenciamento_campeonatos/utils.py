import itertools
from datetime import timedelta
from .models import Rodada, Jogo
from campeonatos.models import Inscricao  # Importar o modelo de Inscrição

def gerar_jogos(campeonato):
    # Resgata todas as inscrições e agrupa os participantes por times
    inscricoes = Inscricao.objects.filter(campeonato=campeonato)
    times = {}

    # Agrupar participantes por times
    for inscricao in inscricoes:
        equipe = inscricao.participante.equipe_participante
        if equipe not in times:
            times[equipe] = []  # Inicializa uma lista para o time se ainda não existir
        times[equipe].append(inscricao.participante)

    equipes = list(times.keys())
    numero_equipes = len(equipes)

    print(f"Times: {equipes}")  # Para verificar a lista de equipes no terminal

    if numero_equipes < 2:
        return "Não há equipes suficientes para gerar jogos."

    # Gera todas as combinações de jogos entre as equipes
    combinacoes = list(itertools.combinations(equipes, 2))
    data_inicial = campeonato.data_inicio

    for i, (equipe_casa, equipe_fora) in enumerate(combinacoes):
        rodada_numero = i // (numero_equipes // 2) + 1
        data_jogo = data_inicial + timedelta(days=rodada_numero * 7)  # Uma rodada por semana

        # Seleciona um participante de cada equipe para o jogo (aqui usamos o primeiro participante de cada equipe)
        time_casa = times[equipe_casa][0]  # Primeiro participante do time da casa
        time_fora = times[equipe_fora][0]  # Primeiro participante do time visitante

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
