from django import forms
from .models import Campeonato

class CampeonatoForm(forms.ModelForm):
    class Meta:
        model = Campeonato
        fields = ['nome', 'data_inicio', 'data_fim', 'descricao', 'premiação']  # Verifique o nome aqui
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'premiacao': forms.NumberInput(attrs={'step': '0.01'}),  # Adiciona o widget de número para premiacao
        }
        
from .models import Inscricao

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome_participante', 'email_participante', 'equipe_participante']
