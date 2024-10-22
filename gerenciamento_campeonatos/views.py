from django.shortcuts import render, get_object_or_404, redirect
from campeonatos.models import Campeonato
from .utils import gerar_jogos
from campeonatos.models import Inscricao  # Importar o modelo de Inscrição
from django.urls import reverse
from campeonatos.models import Campeonato
from gerenciamento_campeonatos.models import Jogo, Resultado


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

    # Inicializa a pontuação de todos os times a partir das inscrições
    inscricoes = Inscricao.objects.filter(campeonato=campeonato)
    times = {}
    
    # Inicializar o dicionário para equipes, agrupando participantes por equipe
    for inscricao in inscricoes:
        equipe = inscricao.participante.equipe_participante
        if equipe not in pontuacao:
            pontuacao[equipe] = {'pontos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}

    # Percorre todos os jogos do campeonato
    for rodada in campeonato.rodadas.all():
        for jogo in rodada.jogos.all():
            # Verifica se o jogo tem um resultado associado
            if hasattr(jogo, 'resultado_jogo') and jogo.resultado_jogo:
                equipe_casa = jogo.time_casa.equipe_participante
                equipe_fora = jogo.time_fora.equipe_participante

                # Atualiza a pontuação das equipes, e não dos participantes
                if jogo.resultado_jogo.gols_time_casa > jogo.resultado_jogo.gols_time_fora:
                    pontuacao[equipe_casa]['pontos'] += 3
                    pontuacao[equipe_casa]['vitorias'] += 1
                    pontuacao[equipe_fora]['derrotas'] += 1
                elif jogo.resultado_jogo.gols_time_casa < jogo.resultado_jogo.gols_time_fora:
                    pontuacao[equipe_fora]['pontos'] += 3
                    pontuacao[equipe_fora]['vitorias'] += 1
                    pontuacao[equipe_casa]['derrotas'] += 1
                else:
                    pontuacao[equipe_casa]['pontos'] += 1
                    pontuacao[equipe_fora]['pontos'] += 1
                    pontuacao[equipe_casa]['empates'] += 1
                    pontuacao[equipe_fora]['empates'] += 1

    return pontuacao

def registrar_resultados(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    jogos = Jogo.objects.filter(rodada__campeonato=campeonato)

    if request.method == 'POST':
        for jogo in jogos:
            gols_time_casa = request.POST.get(f'gols_time_casa_{jogo.id}')
            gols_time_fora = request.POST.get(f'gols_time_fora_{jogo.id}')

            # Verificar se o resultado já existe ou criar um novo
            resultado, created = Resultado.objects.get_or_create(jogo=jogo)
            resultado.gols_time_casa = gols_time_casa
            resultado.gols_time_fora = gols_time_fora
            resultado.save()

        return redirect(reverse('visualizar_tabela', args=[campeonato_id]))

    return render(request, 'registrar_resultados.html', {
        'campeonato': campeonato,
        'jogos': jogos,
    })