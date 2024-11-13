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
from campeonatos.models import Campeonato, Inscricao
from gerenciamento_campeonatos.models import Jogo, Rodada, Resultado, RodadasClassificatorias, RodadaEliminatoria, JogoEliminatorio, ResultadoEliminatorio


def visualizar_desempenho(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    form = SelecionarEquipeForm(campeonato, request.GET or None)

    rodadas = []
    gols_pro = []
    gols_contra = []
    equipe_selecionada = None
    desempenho_dados = False

    if form.is_valid():
        equipe_selecionada = form.cleaned_data['equipe']
        
        # Obter todas as rodadas classificatórias
        todas_rodadas = Rodada.objects.filter(campeonato=campeonato).order_by('numero')
        todas_eliminatorias = RodadaEliminatoria.objects.filter(campeonato=campeonato).order_by('fase')

        # Processar as rodadas classificatórias
        for rodada in todas_rodadas:
            rodadas.append(f'Rodada {rodada.numero}')
            jogo = Jogo.objects.filter(
                rodada=rodada,
                time_casa=equipe_selecionada.participante
            ).first() or Jogo.objects.filter(
                rodada=rodada,
                time_fora=equipe_selecionada.participante
            ).first()

            # Adicionar resultados se houver jogo
            if jogo and hasattr(jogo, 'resultado_jogo'):
                desempenho_dados = True
                resultado = jogo.resultado_jogo
                if jogo.time_casa == equipe_selecionada.participante:
                    gols_pro.append(resultado.gols_time_casa)
                    gols_contra.append(resultado.gols_time_fora)
                else:
                    gols_pro.append(resultado.gols_time_fora)
                    gols_contra.append(resultado.gols_time_casa)
            else:
                gols_pro.append(0)
                gols_contra.append(0)

        # Processar as rodadas eliminatórias
        for eliminatoria in todas_eliminatorias:
            rodadas.append(f'{eliminatoria.get_fase_display()}')
            jogo_eliminatorio = JogoEliminatorio.objects.filter(
                rodada=eliminatoria,
                time_casa=equipe_selecionada.participante
            ).first() or JogoEliminatorio.objects.filter(
                rodada=eliminatoria,
                time_fora=equipe_selecionada.participante
            ).first()

            # Adicionar resultados se houver jogo eliminatório
            if jogo_eliminatorio and hasattr(jogo_eliminatorio, 'resultado_eliminatorio'):
                desempenho_dados = True
                resultado_eliminatorio = jogo_eliminatorio.resultado_eliminatorio
                if jogo_eliminatorio.time_casa == equipe_selecionada.participante:
                    gols_pro.append(resultado_eliminatorio.gols_time_casa)
                    gols_contra.append(resultado_eliminatorio.gols_time_fora)
                else:
                    gols_pro.append(resultado_eliminatorio.gols_time_fora)
                    gols_contra.append(resultado_eliminatorio.gols_time_casa)
            else:
                gols_pro.append(0)
                gols_contra.append(0)

    return render(request, 'visualizar_desempenho.html', {
        'campeonato': campeonato,
        'form': form,
        'rodadas': rodadas,
        'gols_pro': gols_pro,
        'gols_contra': gols_contra,
        'equipe_selecionada': equipe_selecionada,
        'desempenho_dados': desempenho_dados,
    })
