from django import forms
from .models import Campeonato

class CampeonatoForm(forms.ModelForm):
    class Meta:
        model = Campeonato
        fields = ['nome', 'data_inicio', 'data_fim', 'descricao', 'premiação', 'numero_maximo_participantes']
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Alterado para datetime-local
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Alterado para datetime-local
            'premiacao': forms.NumberInput(attrs={'step': '0.01'}),
        }
        
from .models import Inscricao

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome_participante', 'email_participante', 'equipe_participante']
