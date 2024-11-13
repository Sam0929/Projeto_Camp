from django import forms
from campeonatos.models import Campeonato, Inscricao

class SelecionarEquipeForm(forms.Form):
    equipe = forms.ModelChoiceField(queryset=None, label="Equipe")

    def __init__(self, campeonato, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar equipes baseadas nas inscrições do campeonato
        self.fields['equipe'].queryset = Inscricao.objects.filter(campeonato=campeonato).select_related('participante')
