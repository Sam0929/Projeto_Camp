# gerenciamento/forms.py
from django import forms
from .models import RodadasClassificatorias

class EliminatoriasForm(forms.Form):
    tipo_eliminatoria = forms.ChoiceField(
        choices=[
            ('ganhador_unico', 'Ganhador Único'),
            ('oitavas_de_final', 'Oitavas de Final'),
            ('quartas_de_final', 'Quartas de Final'),
            ('semi_finais', 'Semi-finais'),
            ('final', 'Final')
        ]
    )
    
    # Campos de data opcionais, de acordo com o tipo de eliminatória
    data_oitavas = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    data_quartas = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    data_semi = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    data_final = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
