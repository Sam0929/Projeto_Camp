from django.shortcuts import render
from .models import Campeonato

def campeonatos(request):

    campeonatos = Campeonato.objects.all()

    return render(request, 'campeonatos.html', {'campeonatos': campeonatos})


