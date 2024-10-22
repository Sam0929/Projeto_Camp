from django.shortcuts import render, get_object_or_404
from campeonatos.models import Campeonato
from .utils import gerar_jogos

def index(request):
    # Buscando todos os campeonatos da aplicação 'campeonatos'
    campeonatos = Campeonato.objects.all()  
    return render(request, 'gerenciamento_campeonato.html', {'campeonatos': campeonatos})


def gerar_tabela(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    mensagem = gerar_jogos(campeonato)
    return render(request, 'tabela_gerada.html', {'mensagem': mensagem, 'campeonato': campeonato})


def visualizar_tabela(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    pontuacao = calcular_pontuacao(campeonato)
    participantes = campeonato.participantes.all()
    
    return render(request, 'tabela_campeonato.html', {
        'campeonato': campeonato,
        'pontuacao': pontuacao,
        'participantes': participantes,  # Passando participantes para o template
    })


def calcular_pontuacao(campeonato):
    pontuacao = {}

    # Inicializa a pontuação de todos os participantes
    for participante in campeonato.participantes.all():
        pontuacao[participante.nome] = {'pontos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}

    # Percorre todos os jogos do campeonato
    for rodada in campeonato.rodadas.all():
        for jogo in rodada.jogos.all():
            if jogo.resultado_jogo:
                # Calcula pontos baseados nos resultados
                if jogo.resultado_jogo.gols_time_casa > jogo.resultado_jogo.gols_time_fora:
                    pontuacao[jogo.time_casa.nome]['pontos'] += 3
                    pontuacao[jogo.time_casa.nome]['vitorias'] += 1
                    pontuacao[jogo.time_fora.nome]['derrotas'] += 1
                elif jogo.resultado_jogo.gols_time_casa < jogo.resultado_jogo.gols_time_fora:
                    pontuacao[jogo.time_fora.nome]['pontos'] += 3
                    pontuacao[jogo.time_fora.nome]['vitorias'] += 1
                    pontuacao[jogo.time_casa.nome]['derrotas'] += 1
                else:
                    pontuacao[jogo.time_casa.nome]['pontos'] += 1
                    pontuacao[jogo.time_fora.nome]['pontos'] += 1
                    pontuacao[jogo.time_casa.nome]['empates'] += 1
                    pontuacao[jogo.time_fora.nome]['empates'] += 1

    return pontuacao
