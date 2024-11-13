from django.shortcuts import render
from campeonatos.models import Campeonato

def listar_campeonatos(request):
    campeonatos = Campeonato.objects.all()
    campeonatos_com_estado = []
    for campeonato in campeonatos:
        tabela_gerada = campeonato.rodadas.exists()
        campeonatos_com_estado.append({
            'campeonato': campeonato,
            'tabela_gerada': tabela_gerada
        })

    return render(request, 'listar_campeonatos.html', {'campeonatos_com_estado': campeonatos_com_estado})

from django.shortcuts import render, get_object_or_404
from campeonatos.models import Campeonato, Participante
from gerenciamento_campeonatos.models import Jogo, Resultado
from django import forms

class SelecionarEquipeForm(forms.Form):
    equipe = forms.ModelChoiceField(queryset=Participante.objects.none(), label='Escolha uma equipe')

    def __init__(self, campeonato, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['equipe'].queryset = Participante.objects.filter(campeonato=campeonato)


from django.shortcuts import get_object_or_404, render
from .forms import SelecionarEquipeForm
from campeonatos.models import Campeonato, Inscricao, Participante
from gerenciamento_campeonatos.models import Jogo, Rodada, Resultado, RodadaEliminatoria, JogoEliminatorio

def visualizar_desempenho(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    form = SelecionarEquipeForm(campeonato, request.GET or None)

    rodadas = []
    gols_pro = []
    gols_contra = []
    equipe_selecionada = None
    desempenho_dados = False
    detalhes = {}

    equipes = {}
    for inscricao in Inscricao.objects.filter(campeonato=campeonato).select_related('participante'):
        equipe_nome = inscricao.participante.equipe
        if equipe_nome not in equipes:
            equipes[equipe_nome] = {'participante': None, 'dados_disponiveis': False}
        tem_dados = Jogo.objects.filter(time_casa=inscricao.participante).exists() or \
                    Jogo.objects.filter(time_fora=inscricao.participante).exists()
        if tem_dados:
            equipes[equipe_nome] = {'participante': inscricao.participante, 'dados_disponiveis': True}

    if form.is_valid():
        equipe_selecionada = form.cleaned_data['equipe']
        participante = equipes[equipe_selecionada]['participante']
        
        todas_rodadas = Rodada.objects.filter(campeonato=campeonato).order_by('numero')
        todas_eliminatorias = RodadaEliminatoria.objects.filter(campeonato=campeonato).order_by('fase')

        for rodada in todas_rodadas:
            rodadas.append(f'Rodada {rodada.numero}')
            jogo = Jogo.objects.filter(
                rodada=rodada,
                time_casa=participante
            ).first() or Jogo.objects.filter(
                rodada=rodada,
                time_fora=participante
            ).first()

            if jogo and hasattr(jogo, 'resultado_jogo'):
                desempenho_dados = True
                resultado = jogo.resultado_jogo
                if jogo.time_casa == participante:
                    gols_pro.append(resultado.gols_time_casa)
                    gols_contra.append(resultado.gols_time_fora)
                else:
                    gols_pro.append(resultado.gols_time_fora)
                    gols_contra.append(resultado.gols_time_casa)
            else:
                gols_pro.append(0)
                gols_contra.append(0)

        fase_order = {'oitavas_de_final': 0, 'quartas_de_final': 1, 'semi_finais': 2, 'final': 3}
        eliminatorias_ordenadas = sorted(todas_eliminatorias, key=lambda e: fase_order.get(e.fase, 4))

        for eliminatoria in eliminatorias_ordenadas:
            rodadas.append(f'{eliminatoria.get_fase_display()}')
            jogo_eliminatorio = JogoEliminatorio.objects.filter(
                rodada=eliminatoria,
                time_casa=participante
            ).first() or JogoEliminatorio.objects.filter(
                rodada=eliminatoria,
                time_fora=participante
            ).first()

            if jogo_eliminatorio and hasattr(jogo_eliminatorio, 'resultado_eliminatorio'):
                desempenho_dados = True
                resultado_eliminatorio = jogo_eliminatorio.resultado_eliminatorio
                if jogo_eliminatorio.time_casa == participante:
                    gols_pro.append(resultado_eliminatorio.gols_time_casa)
                    gols_contra.append(resultado_eliminatorio.gols_time_fora)
                else:
                    gols_pro.append(resultado_eliminatorio.gols_time_fora)
                    gols_contra.append(resultado_eliminatorio.gols_time_casa)
            else:
                gols_pro.append(0)
                gols_contra.append(0)

        detalhes = detalhar_desempenho(participante, campeonato)

    return render(request, 'visualizar_desempenho.html', {
        'campeonato': campeonato,
        'form': form,
        'rodadas': rodadas,
        'gols_pro': gols_pro,
        'gols_contra': gols_contra,
        'equipe_selecionada': equipe_selecionada,
        'desempenho_dados': desempenho_dados,
        'saldo_pontos': detalhes.get('saldo_pontos', 0),
        'vitorias': detalhes.get('vitorias', 0),
        'empates': detalhes.get('empates', 0),
        'derrotas': detalhes.get('derrotas', 0),
        'historico_jogos': detalhes.get('historico_jogos', []),
        'classificado_eliminatorias': detalhes.get('classificado_eliminatorias', False),
    })


def detalhar_desempenho(equipe_selecionada, campeonato):
    saldo_pontos = 0
    vitorias, empates, derrotas = 0, 0, 0
    historico_jogos = []
    classificado_eliminatorias = False
    
    # Obtém todas as rodadas classificatórias e eliminatórias
    todas_rodadas = Rodada.objects.filter(campeonato=campeonato).order_by('numero')
    todas_eliminatorias = RodadaEliminatoria.objects.filter(campeonato=campeonato).order_by('fase')

    # Processa rodadas classificatórias
    for rodada in todas_rodadas:
        jogo = Jogo.objects.filter(
            rodada=rodada,
            time_casa=equipe_selecionada
        ).first() or Jogo.objects.filter(
            rodada=rodada,
            time_fora=equipe_selecionada
        ).first()

        if jogo and hasattr(jogo, 'resultado_jogo'):
            resultado = jogo.resultado_jogo
            if jogo.time_casa == equipe_selecionada:
                pontos_pro = resultado.gols_time_casa
                pontos_contra = resultado.gols_time_fora
                adversario = jogo.time_fora.equipe
            else:
                pontos_pro = resultado.gols_time_fora
                pontos_contra = resultado.gols_time_casa
                adversario = jogo.time_casa.equipe
            
            saldo_pontos += pontos_pro - pontos_contra
            historico_jogos.append({
                'rodada': rodada.numero,
                'fase': None,  # Adiciona `fase` como None para rodadas normais
                'adversario': adversario,
                'pontos_pro': pontos_pro,
                'pontos_contra': pontos_contra,
            })

            # Contabiliza vitórias, empates e derrotas
            if pontos_pro > pontos_contra:
                vitorias += 1
            elif pontos_pro == pontos_contra:
                empates += 1
            else:
                derrotas += 1

    # Processa rodadas eliminatórias
    fase_order = {'oitavas_de_final': 0, 'quartas_de_final': 1, 'semi_finais': 2, 'final': 3}
    eliminatorias_ordenadas = sorted(todas_eliminatorias, key=lambda e: fase_order.get(e.fase, 4))

    for eliminatoria in eliminatorias_ordenadas:
        jogo_eliminatorio = JogoEliminatorio.objects.filter(
            rodada=eliminatoria,
            time_casa=equipe_selecionada
        ).first() or JogoEliminatorio.objects.filter(
            rodada=eliminatoria,
            time_fora=equipe_selecionada
        ).first()

        if jogo_eliminatorio and hasattr(jogo_eliminatorio, 'resultado_eliminatorio'):
            classificado_eliminatorias = True
            resultado_eliminatorio = jogo_eliminatorio.resultado_eliminatorio
            if jogo_eliminatorio.time_casa == equipe_selecionada:
                pontos_pro = resultado_eliminatorio.gols_time_casa
                pontos_contra = resultado_eliminatorio.gols_time_fora
                adversario = jogo_eliminatorio.time_fora.equipe
            else:
                pontos_pro = resultado_eliminatorio.gols_time_fora
                pontos_contra = resultado_eliminatorio.gols_time_casa
                adversario = jogo_eliminatorio.time_casa.equipe

            saldo_pontos += pontos_pro - pontos_contra
            historico_jogos.append({
                'rodada': None,  # Define como None, pois é uma rodada eliminatória
                'fase': eliminatoria.get_fase_display(),  # Nome da fase eliminatória
                'adversario': adversario,
                'pontos_pro': pontos_pro,
                'pontos_contra': pontos_contra,
            })

            if pontos_pro > pontos_contra:
                vitorias += 1
            elif pontos_pro == pontos_contra:
                empates += 1
            else:
                derrotas += 1

    return {
        'saldo_pontos': saldo_pontos,
        'vitorias': vitorias,
        'empates': empates,
        'derrotas': derrotas,
        'historico_jogos': historico_jogos,
        'classificado_eliminatorias': classificado_eliminatorias
    }
