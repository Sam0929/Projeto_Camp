import datetime
from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from sistema_campeonatos.middleware import admin_required
from .forms import EliminatoriasForm
from campeonatos.models import Campeonato, Participante
from .models import Jogo, Resultado, Penalidade, JogoEliminatorio, ResultadoEliminatorio, RodadaEliminatoria, PenalidadeEliminatoria
from .utils import gerar_jogos
from campeonatos.models import Inscricao  # Importar o modelo de Inscrição
from django.urls import reverse
from campeonatos.models import Campeonato


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

@admin_required
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

    for inscricao in inscricoes:
        equipe = inscricao.participante.equipe
        if equipe not in pontuacao:
            pontuacao[equipe] = {'pontos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0, 'gols_marcados': 0, 'gols_sofridos': 0, 'saldo_gols': 0, 'confrontos_diretos': {}}

    # Percorre todos os jogos do campeonato
    for rodada in campeonato.rodadas.all():
        for jogo in rodada.jogos.all():
            if hasattr(jogo, 'resultado_jogo') and jogo.resultado_jogo:
                gols_time_casa = jogo.resultado_jogo.gols_time_casa
                gols_time_fora = jogo.resultado_jogo.gols_time_fora

                equipe_casa = jogo.time_casa.equipe
                equipe_fora = jogo.time_fora.equipe

                if gols_time_casa is not None and gols_time_fora is not None:
                    # Atualizar gols marcados, sofridos e saldo de gols
                    pontuacao[equipe_casa]['gols_marcados'] += gols_time_casa
                    pontuacao[equipe_casa]['gols_sofridos'] += gols_time_fora
                    pontuacao[equipe_fora]['gols_marcados'] += gols_time_fora
                    pontuacao[equipe_fora]['gols_sofridos'] += gols_time_casa

                    pontuacao[equipe_casa]['saldo_gols'] = pontuacao[equipe_casa]['gols_marcados'] - pontuacao[equipe_casa]['gols_sofridos']
                    pontuacao[equipe_fora]['saldo_gols'] = pontuacao[equipe_fora]['gols_marcados'] - pontuacao[equipe_fora]['gols_sofridos']

                    # Atualiza pontos e resultados (vitória, empate, derrota)
                    if gols_time_casa > gols_time_fora:
                        pontuacao[equipe_casa]['pontos'] += 3
                        pontuacao[equipe_casa]['vitorias'] += 1
                        pontuacao[equipe_fora]['derrotas'] += 1
                    elif gols_time_casa < gols_time_fora:
                        pontuacao[equipe_fora]['pontos'] += 3
                        pontuacao[equipe_fora]['vitorias'] += 1
                        pontuacao[equipe_casa]['derrotas'] += 1
                    else:
                        pontuacao[equipe_casa]['pontos'] += 1
                        pontuacao[equipe_fora]['pontos'] += 1
                        pontuacao[equipe_casa]['empates'] += 1
                        pontuacao[equipe_fora]['empates'] += 1

                    # Atualiza confrontos diretos
                    if equipe_fora not in pontuacao[equipe_casa]['confrontos_diretos']:
                        pontuacao[equipe_casa]['confrontos_diretos'][equipe_fora] = 0
                    if equipe_casa not in pontuacao[equipe_fora]['confrontos_diretos']:
                        pontuacao[equipe_fora]['confrontos_diretos'][equipe_casa] = 0

                    # Confronto direto: +1 para vitória, -1 para derrota
                    if gols_time_casa > gols_time_fora:
                        pontuacao[equipe_casa]['confrontos_diretos'][equipe_fora] += 1
                        pontuacao[equipe_fora]['confrontos_diretos'][equipe_casa] -= 1
                    elif gols_time_casa < gols_time_fora:
                        pontuacao[equipe_fora]['confrontos_diretos'][equipe_casa] += 1
                        pontuacao[equipe_casa]['confrontos_diretos'][equipe_fora] -= 1

    # Ordenar por pontos, saldo de gols, gols marcados e confrontos diretos
    pontuacao_ordenada = sorted(
        pontuacao.items(),
        key=lambda item: (item[1]['pontos'], item[1]['saldo_gols'], item[1]['gols_marcados']),
        reverse=True
    )

    return dict(pontuacao_ordenada)


@admin_required
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

@admin_required
def registrar_penalidades(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    jogos = Jogo.objects.filter(rodada__campeonato=campeonato)
    participantes = Participante.objects.filter(campeonato=campeonato)

    if request.method == 'POST':
        jogo_id = request.POST.get('jogo_id')
        tipo_penalidade = request.POST.get('tipo_cartao')
        alvo_penalidade = request.POST.get('tipo_penalidade')
        participante_id = request.POST.get('participante_id') if alvo_penalidade == 'participante' else None
        equipe = request.POST.get('equipe') if alvo_penalidade == 'equipe' else None
        motivo = request.POST.get('motivo')

        jogo = get_object_or_404(Jogo, id=jogo_id)
        participante = get_object_or_404(Participante, id=participante_id) if participante_id else None

        # Criar nova penalidade
        penalidade = Penalidade(
            jogo=jogo,
            tipo_penalidade=tipo_penalidade,
            participante=participante,
            equipe=equipe,
            motivo=motivo
        )
        penalidade.save()

        return redirect(reverse('visualizar_tabela', args=[campeonato_id]))

    return render(request, 'registrar_penalidades.html', {
        'campeonato': campeonato,
        'jogos': jogos,
        'participantes': participantes,
    })

@admin_required
def confirmar_classificacao(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)

    # Verificar se todos os jogos possuem resultados
    jogos_sem_resultado = Jogo.objects.filter(
        rodada__campeonato=campeonato,
        resultado_jogo__isnull=True
    ).exists()

    if request.method == 'POST':
        # Se o botão confirmar foi clicado
        if 'confirmar' in request.POST:
            # Redireciona para gerar_classificacao independentemente de jogos sem resultado
            return redirect(reverse('gerar_classificacao', args=[campeonato_id]))
        
        # Se o botão cancelar foi clicado
        elif 'cancelar' in request.POST:
            return redirect(reverse('visualizar_tabela', args=[campeonato_id]))

    # Renderiza a página de confirmação inicialmente
    return render(request, 'confirmar_classificacao.html', {'campeonato': campeonato, 'jogos_sem_resultado': jogos_sem_resultado})

@admin_required
def gerar_classificacao(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)

    if request.method == 'POST':
        # Obtém o número de classificados enviado pelo formulário
        num_classificados = int(request.POST.get('num_classificados', 4))
        request.session['num_classificados'] = num_classificados  # Armazena na sessão

        # Marca a classificação como gerada no modelo e salva
        campeonato.classificacao_gerada = True
        campeonato.save()

        # Redireciona para a visualização da classificação
        return redirect(reverse('visualizar_classificacao', args=[campeonato_id]))

    # Renderiza o formulário para inserir o número de classificados
    return render(request, 'gerar_classificacao.html', {'campeonato': campeonato})


def visualizar_classificacao(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    pontuacao = calcular_pontuacao(campeonato)

    # Ordena os times de acordo com pontuação
    classificados = sorted(
        pontuacao.items(),
        key=lambda item: (item[1]['pontos'], item[1]['saldo_gols'], item[1]['gols_marcados']),
        reverse=True
    )

    # Número de classificados (carregado da sessão)
    num_classificados = int(request.session.get('num_classificados', 4))  # valor padrão se não estiver na sessão
    equipes_classificadas = classificados[:num_classificados]
    equipes_desclassificadas = classificados[num_classificados:]

    return render(request, 'classificacao.html', {
        'campeonato': campeonato,
        'classificados': classificados,
        'equipes_classificadas': equipes_classificadas,
        'equipes_desclassificadas': equipes_desclassificadas,
        'num_classificados': num_classificados
    })

@admin_required
def editar_classificacao(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)

    if request.method == 'POST':
        # Atualiza o número de classificados com o novo valor
        num_classificados = int(request.POST.get('num_classificados', 4))
        request.session['num_classificados'] = num_classificados

        # Redireciona para a visualização da classificação atualizada
        return redirect(reverse('visualizar_classificacao', args=[campeonato_id]))

    # Renderiza o formulário de edição de classificação
    return render(request, 'editar_classificacao.html', {'campeonato': campeonato})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Campeonato, RodadasClassificatorias, Rodada, Jogo
from .forms import EliminatoriasForm

@admin_required
def configurar_eliminatorias(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    
    # Verifica se as eliminatórias já foram geradas
    if campeonato.eliminatorias_geradas:
        # Se já foram geradas, redireciona para visualizar as eliminatórias
        return redirect('visualizar_chave_confrontos', campeonato_id=campeonato.id)

    # Obtém a última rodada para definir a data do último jogo
    ultima_rodada = campeonato.rodadas.order_by('-data').first()
    data_ultimo_jogo = ultima_rodada.data if ultima_rodada else None

    # Determina o número de classificados para as eliminatórias
    num_classificados = int(request.session.get('num_classificados', 4))
    if 'num_classificados' not in request.session:
        pontuacao = calcular_pontuacao(campeonato)
        num_classificados = len(pontuacao)
        request.session['num_classificados'] = num_classificados

    if request.method == 'POST':
        # Gera as eliminatórias apenas se elas ainda não foram geradas
        tipo = request.POST.get('tipo_eliminatoria')
        datas_horas_fases = {
            'oitavas_de_final': f"{request.POST.get('data_oitavas')} {request.POST.get('hora_oitavas')}",
            'quartas_de_final': f"{request.POST.get('data_quartas')} {request.POST.get('hora_quartas')}",
            'semi_finais': f"{request.POST.get('data_semi')} {request.POST.get('hora_semi')}",
            'final': f"{request.POST.get('data_final')} {request.POST.get('hora_final')}",
        }
        gerar_fases_eliminatorias(campeonato, tipo, datas_horas_fases)
        
        # Marca as eliminatórias como geradas
        campeonato.eliminatorias_geradas = True
        campeonato.save()

        return redirect('visualizar_chave_confrontos', campeonato_id=campeonato.id)

    context = {
        'campeonato': campeonato,
        'data_ultimo_jogo': data_ultimo_jogo,
        'num_classificados': num_classificados,
    }
    return render(request, 'configurar_eliminatorias.html', context)



def gerar_fases_eliminatorias(campeonato, tipo_eliminatoria, datas_horas_fases):
    pontuacao = calcular_pontuacao(campeonato)
    classificados = [
        equipe for equipe, dados in sorted(
            pontuacao.items(),
            key=lambda item: (item[1]['pontos'], item[1]['saldo_gols'], item[1]['gols_marcados']),
            reverse=True
        )[:16]
    ]

    min_classificados = {
        'oitavas_de_final': 16,
        'quartas_de_final': 8,
        'semi_finais': 4,
        'final': 2,
    }

    if len(classificados) < min_classificados.get(tipo_eliminatoria, 2):
        raise ValueError(f"Número insuficiente de participantes para {tipo_eliminatoria}. Necessário: {min_classificados[tipo_eliminatoria]}")

    for fase, num_classificados in min_classificados.items():
        if min_classificados[tipo_eliminatoria] >= num_classificados:
            data = datas_horas_fases.get(fase)  # Usando 'data' para o campo correto
            if data:
                rodada_eliminatoria = RodadaEliminatoria.objects.create(
                    campeonato=campeonato,
                    fase=fase,
                    data=data  # Atualizado para usar o nome correto do campo
                )

                num_confrontos = num_classificados // 2
                for i in range(num_confrontos):
                    if fase == tipo_eliminatoria:
                        time_casa = Participante.objects.filter(equipe=classificados[i * 2]).first()
                        time_fora = Participante.objects.filter(equipe=classificados[i * 2 + 1]).first()
                    else:
                        time_casa = None
                        time_fora = None

                    JogoEliminatorio.objects.create(
                        rodada=rodada_eliminatoria,
                        time_casa=time_casa,
                        time_fora=time_fora,
                        placeholder=True if not time_casa or not time_fora else False
                    )

def visualizar_chave_confrontos(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    rodadas_eliminatorias = RodadaEliminatoria.objects.filter(campeonato=campeonato).order_by('fase')
    
    # Define a ordem das fases
    ordem_fases = ['oitavas_de_final', 'quartas_de_final', 'semi_finais', 'final']
    jogos_por_rodada = {}
    vencedor_final = None

    for fase in ordem_fases:
        rodada = rodadas_eliminatorias.filter(fase=fase).first()
        if rodada:
            jogos = JogoEliminatorio.objects.filter(rodada=rodada)
            jogos_por_rodada[rodada.get_fase_display()] = jogos
            
            # Verifica o vencedor da final
            if fase == 'final' and jogos.exists():
                jogo_final = jogos.first()
                if hasattr(jogo_final, 'resultado_eliminatorio') and jogo_final.resultado_eliminatorio:
                    if jogo_final.resultado_eliminatorio.gols_time_casa > jogo_final.resultado_eliminatorio.gols_time_fora:
                        vencedor_final = jogo_final.time_casa.equipe
                    elif jogo_final.resultado_eliminatorio.gols_time_fora > jogo_final.resultado_eliminatorio.gols_time_casa:
                        vencedor_final = jogo_final.time_fora.equipe

    return render(request, 'chave_confrontos.html', {
        'campeonato': campeonato,
        'jogos_por_rodada': jogos_por_rodada,
        'vencedor_final': vencedor_final,
        'premiacao': campeonato.premiação,
    })


def visualizar_ganhador_unico(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    pontuacao = calcular_pontuacao(campeonato)
    
    vencedor = sorted(
        pontuacao.items(),
        key=lambda item: (item[1]['pontos'], item[1]['saldo_gols'], item[1]['gols_marcados']),
        reverse=True
    )[0][0]  # Seleciona o primeiro colocado
    
    return render(request, 'ganhador_unico.html', {'vencedor': vencedor, 'campeonato': campeonato})

@admin_required
def registrar_resultados_eliminatorias(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    jogos = JogoEliminatorio.objects.filter(rodada__campeonato=campeonato)

    if request.method == 'POST':
        jogo_id = request.POST.get('jogo_selecionado')
        gols_time_casa = request.POST.get('gols_time_casa')
        gols_time_fora = request.POST.get('gols_time_fora')

        if jogo_id:
            jogo = get_object_or_404(JogoEliminatorio, id=jogo_id)
            if gols_time_casa.isdigit() and gols_time_fora.isdigit():
                gols_time_casa = int(gols_time_casa)
                gols_time_fora = int(gols_time_fora)

                # Salva o resultado
                resultado, created = ResultadoEliminatorio.objects.get_or_create(jogo=jogo)
                resultado.gols_time_casa = gols_time_casa
                resultado.gols_time_fora = gols_time_fora
                resultado.save()

                # Determina o vencedor e passa para a próxima fase
                if gols_time_casa > gols_time_fora:
                    vencedor = jogo.time_casa
                elif gols_time_fora > gols_time_casa:
                    vencedor = jogo.time_fora
                else:
                    vencedor = None  # Empates podem ser tratados de acordo com regras do campeonato

                if vencedor:
                    proxima_fase = definir_proxima_fase(jogo.rodada.fase)
                    if proxima_fase:
                        alocar_vencedor_para_proxima_fase(campeonato, proxima_fase, vencedor)

                return redirect(reverse('visualizar_chave_confrontos', args=[campeonato_id]))

    return render(request, 'registrar_resultados_eliminatorias.html', {
        'campeonato': campeonato,
        'jogos': jogos,
    })


def definir_proxima_fase(fase_atual):
    fases_ordenadas = ['oitavas_de_final', 'quartas_de_final', 'semi_finais', 'final']
    try:
        indice_fase = fases_ordenadas.index(fase_atual)
        return fases_ordenadas[indice_fase + 1] if indice_fase + 1 < len(fases_ordenadas) else None
    except ValueError:
        return None

def alocar_vencedor_para_proxima_fase(campeonato, fase, vencedor):
    rodada_proxima_fase, created = RodadaEliminatoria.objects.get_or_create(
        campeonato=campeonato,
        fase=fase,
    )
    # Busca um jogo vazio (sem participantes) na próxima fase para alocar o vencedor
    jogo = JogoEliminatorio.objects.filter(rodada=rodada_proxima_fase, time_casa__isnull=True).first()
    if jogo:
        jogo.time_casa = vencedor
    else:
        jogo = JogoEliminatorio.objects.filter(rodada=rodada_proxima_fase, time_fora__isnull=True).first()
        if jogo:
            jogo.time_fora = vencedor
    jogo.save()

@admin_required
def registrar_penalidades_eliminatorias(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    jogos = JogoEliminatorio.objects.filter(rodada__campeonato=campeonato)
    participantes = Participante.objects.filter(campeonato=campeonato)

    if request.method == 'POST':
        jogo_id = request.POST.get('jogo_id')
        tipo_penalidade = request.POST.get('tipo_cartao')
        alvo_penalidade = request.POST.get('tipo_penalidade')
        participante_id = request.POST.get('participante_id') if alvo_penalidade == 'participante' else None
        motivo = request.POST.get('motivo')  # Recebe o motivo da penalidade

        jogo = get_object_or_404(JogoEliminatorio, id=jogo_id)
        participante = get_object_or_404(Participante, id=participante_id) if participante_id else None

        # Criar nova penalidade eliminatória
        penalidade_eliminatoria = PenalidadeEliminatoria(
            jogo=jogo,
            tipo_penalidade=tipo_penalidade,
            participante=participante,
            motivo=motivo  # Salva o motivo da penalidade
        )
        penalidade_eliminatoria.save()

        return redirect(reverse('visualizar_chave_confrontos', args=[campeonato_id]))

    return render(request, 'registrar_penalidades_eliminatorias.html', {
        'campeonato': campeonato,
        'jogos': jogos,
        'participantes': participantes,
    })

