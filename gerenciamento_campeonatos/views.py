from django.shortcuts import render, get_object_or_404, redirect
from campeonatos.models import Campeonato
from .utils import gerar_jogos
from campeonatos.models import Inscricao  # Importar o modelo de Inscrição
from django.urls import reverse
from campeonatos.models import Campeonato
from gerenciamento_campeonatos.models import Jogo, Resultado
from datetime import timedelta
from collections import defaultdict


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

    # Cálculo da duração do campeonato em dias
    duracao_campeonato = (campeonato.data_fim - campeonato.data_inicio).days

    # Cálculo padrão da recomendação de rodadas com base no intervalo de dias
    rodadas_recomendadas = 1  # Valor padrão caso não tenha POST
    
    if request.method == 'POST':
        # Pegando os dados do formulário
        numero_rodadas = int(request.POST.get('numero_rodadas'))
        intervalo_dias = int(request.POST.get('intervalo_dias'))
        horario_inicio = request.POST.get('horario_inicio')
        horario_final = request.POST.get('horario_final')
        duracao_partida = int(request.POST.get('duracao_partida'))
        intervalo_jogos = int(request.POST.get('intervalo_jogos'))
        dias_preferencia = request.POST.getlist('dias_preferencia')  # Lista com os dias preferenciais

        # Gera os jogos com base nas opções do usuário
        mensagem = gerar_jogos(
            campeonato,
            numero_rodadas,
            intervalo_dias,
            horario_inicio,
            horario_final,
            duracao_partida,
            intervalo_jogos,
            dias_preferencia
        )

        if "sucesso" in mensagem.lower():  # Verifica se a geração dos jogos foi bem-sucedida
            # Redireciona para visualizar a tabela após gerar os jogos
            return redirect(reverse('visualizar_tabela', args=[campeonato_id]))
        else:
            # Caso haja uma mensagem de erro na geração dos jogos
            return render(request, 'tabela_gerada.html', {
                'campeonato': campeonato,
                'mensagem': mensagem,
            })
    
    # Cálculo de recomendação de rodadas com base na duração do campeonato e intervalo de dias
    if request.method != 'POST':
        # Caso seja a primeira vez que a página é carregada (sem dados de POST), calcular a recomendação
        rodadas_recomendadas = max(1, duracao_campeonato // 7)  # Exemplo: 1 rodada por semana

    return render(
        request, 
        'gerar_tabela.html', 
        {
            'campeonato': campeonato,
            'duracao_campeonato': duracao_campeonato,
            'rodadas_recomendadas': rodadas_recomendadas,
            'horario_inicio': campeonato.data_inicio.time(),  # Adicionando o horário de início
            'horario_fim': campeonato.data_fim.time(),  # Adicionando o horário de fim
        }
    )


def visualizar_tabela(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    pontuacao = calcular_pontuacao(campeonato)

    # Resgatar os participantes através das inscrições
    inscricoes = Inscricao.objects.filter(campeonato=campeonato)
    
    # Agrupar participantes por equipe
    equipes_participantes = {}
    for inscricao in inscricoes:
        equipe = inscricao.participante.equipe  # Substituído "equipe_participante" por "equipe"
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

    # Inicializar o dicionário para equipes, agrupando participantes por equipe
    for inscricao in inscricoes:
        equipe = inscricao.participante.equipe
        if equipe not in pontuacao:
            pontuacao[equipe] = {'pontos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0}

    # Percorre todos os jogos do campeonato
    for rodada in campeonato.rodadas.all():
        for jogo in rodada.jogos.all():
            if hasattr(jogo, 'resultado_jogo') and jogo.resultado_jogo:
                gols_time_casa = jogo.resultado_jogo.gols_time_casa
                gols_time_fora = jogo.resultado_jogo.gols_time_fora
                
                # Atualiza a pontuação das equipes, e não dos participantes
                if gols_time_casa is not None and gols_time_fora is not None:
                    if gols_time_casa > gols_time_fora:
                        pontuacao[jogo.time_casa.equipe]['pontos'] += 3
                        pontuacao[jogo.time_casa.equipe]['vitorias'] += 1
                        pontuacao[jogo.time_fora.equipe]['derrotas'] += 1
                    elif gols_time_casa < gols_time_fora:
                        pontuacao[jogo.time_fora.equipe]['pontos'] += 3
                        pontuacao[jogo.time_fora.equipe]['vitorias'] += 1
                        pontuacao[jogo.time_casa.equipe]['derrotas'] += 1
                    else:
                        pontuacao[jogo.time_casa.equipe]['pontos'] += 1
                        pontuacao[jogo.time_fora.equipe]['pontos'] += 1
                        pontuacao[jogo.time_casa.equipe]['empates'] += 1
                        pontuacao[jogo.time_fora.equipe]['empates'] += 1

    # Ordenar por pontos (do maior para o menor)
    pontuacao_ordenada = dict(sorted(pontuacao.items(), key=lambda item: item[1]['pontos'], reverse=True))

    return pontuacao_ordenada





def registrar_resultados(request, campeonato_id):
    # Obter o campeonato ou retornar 404
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    
    # Filtrar jogos do campeonato
    jogos = Jogo.objects.filter(rodada__campeonato=campeonato)

    if request.method == 'POST':
        jogo_id = request.POST.get('jogo_selecionado')
        gols_time_casa = request.POST.get('gols_time_casa')
        gols_time_fora = request.POST.get('gols_time_fora')

        # Verificar se um jogo foi selecionado
        if jogo_id:
            jogo = get_object_or_404(Jogo, id=jogo_id)

            # Verificar se os gols são válidos
            if gols_time_casa.isdigit():
                gols_time_casa = int(gols_time_casa)
            else:
                gols_time_casa = None
            
            if gols_time_fora.isdigit():
                gols_time_fora = int(gols_time_fora)
            else:
                gols_time_fora = None

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
