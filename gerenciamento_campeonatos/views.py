from django.shortcuts import render, get_object_or_404
from campeonatos.models import Campeonato
from .utils import gerar_jogos
from campeonatos.models import Inscricao  # Importar o modelo de Inscrição


def index(request):
    campeonatos = Campeonato.objects.all()

    # Adiciona um campo para verificar se a tabela já foi gerada
    campeonatos_com_estado = []
    for campeonato in campeonatos:
        tabela_gerada = campeonato.rodadas.exists()  # Verifica se o campeonato tem rodadas
        campeonatos_com_estado.append({
            'campeonato': campeonato,
            'tabela_gerada': tabela_gerada
        })
    
    return render(request, 'gerenciamento_campeonato.html', {'campeonatos_com_estado': campeonatos_com_estado})


def gerar_tabela(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    mensagem = gerar_jogos(campeonato)
    return render(request, 'tabela_gerada.html', {'mensagem': mensagem, 'campeonato': campeonato})


def visualizar_tabela(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    pontuacao = calcular_pontuacao(campeonato)

    # Resgatar os participantes através das inscrições
    inscricoes = Inscricao.objects.filter(campeonato=campeonato)
    
    # Agrupar participantes por equipe
    equipes_participantes = {}
    for inscricao in inscricoes:
        equipe = inscricao.participante.equipe_participante
        if equipe not in equipes_participantes:
            equipes_participantes[equipe] = []
        equipes_participantes[equipe].append(inscricao.participante)
    
    return render(request, 'tabela_campeonato.html', {
        'campeonato': campeonato,
        'pontuacao': pontuacao,
        'equipes_participantes': equipes_participantes,  # Passando equipes com seus respectivos participantes
    })



def calcular_pontuacao(campeonato):
    pontuacao = {}

    # Inicializa a pontuação de todos os participantes a partir das inscrições
    inscricoes = Inscricao.objects.filter(campeonato=campeonato)
    participantes = [inscricao.participante for inscricao in inscricoes]

    # Inicializa a pontuação para cada equipe participante
    for participante in participantes:
        pontuacao[participante] = {'pontos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}

    # Percorre todos os jogos do campeonato
    for rodada in campeonato.rodadas.all():
        for jogo in rodada.jogos.all():
            # Verifica se o jogo tem um resultado associado
            if hasattr(jogo, 'resultado_jogo') and jogo.resultado_jogo:
                if jogo.resultado_jogo.gols_time_casa > jogo.resultado_jogo.gols_time_fora:
                    pontuacao[jogo.time_casa]['pontos'] += 3
                    pontuacao[jogo.time_casa]['vitorias'] += 1
                    pontuacao[jogo.time_fora]['derrotas'] += 1
                elif jogo.resultado_jogo.gols_time_casa < jogo.resultado_jogo.gols_time_fora:
                    pontuacao[jogo.time_fora]['pontos'] += 3
                    pontuacao[jogo.time_fora]['vitorias'] += 1
                    pontuacao[jogo.time_casa]['derrotas'] += 1
                else:
                    pontuacao[jogo.time_casa]['pontos'] += 1
                    pontuacao[jogo.time_fora]['pontos'] += 1
                    pontuacao[jogo.time_casa]['empates'] += 1
                    pontuacao[jogo.time_fora]['empates'] += 1

    return pontuacao

