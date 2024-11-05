from django import forms
from .models import Campeonato, Inscricao, Participante

class CampeonatoForm(forms.ModelForm):
    class Meta:
        model = Campeonato
        fields = ['nome', 'data_inicio', 'data_fim', 'descricao', 'premiação', 'numero_maximo_participantes']
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Alterado para datetime-local
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),     # Alterado para datetime-local
            'premiacao': forms.NumberInput(attrs={'step': '0.01'}),
        }

class InscricaoForm(forms.ModelForm):
    participante = forms.ModelChoiceField(queryset=Participante.objects.all(), label='Participante')

    class Meta:
        model = Inscricao
        fields = ['participante']

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'email', 'equipe']