from django import forms
from campeonatos.models import Campeonato, Inscricao

class SelecionarEquipeForm(forms.Form):
    equipe = forms.ChoiceField(label="Equipe")

    def __init__(self, campeonato, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obter equipes únicas
        inscricoes = Inscricao.objects.filter(campeonato=campeonato).select_related('participante')
        equipes_unicas = {}
        for inscricao in inscricoes:
            equipe_nome = inscricao.participante.equipe
            if equipe_nome not in equipes_unicas:
                equipes_unicas[equipe_nome] = equipe_nome
        self.fields['equipe'].choices = [(equipe, equipe) for equipe in equipes_unicas.keys()]
