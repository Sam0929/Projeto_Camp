from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Campeonato
from django.http import HttpResponse
from .forms import CampeonatoForm
from django.contrib import messages

def campeonatos(request):

    campeonatos = Campeonato.objects.all()

    return render(request, 'campeonatos.html', {'campeonatos': campeonatos})

def criar_campeonato(request):
    if request.method == 'POST':
        form = CampeonatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campeonatos')  # Redireciona para a lista de campeonatos após a criação
    else:
        form = CampeonatoForm()

    return render(request, 'criar_campeonato.html', {'form': form})

def editar_campeonato(request, pk):
    campeonato = get_object_or_404(Campeonato, pk=pk)
    if request.method == 'POST':
        form = CampeonatoForm(request.POST, instance=campeonato)
        if form.is_valid():
            form.save()
            return redirect('campeonatos')  # Redireciona para a lista de campeonatos
    else:
        form = CampeonatoForm(instance=campeonato)
    
    return render(request, 'editar_campeonato.html', {'form': form})

def deletar_campeonato(request, pk):
    campeonato = get_object_or_404(Campeonato, pk=pk)
    if request.method == 'POST':
        campeonato.delete()
        return redirect('campeonatos')  # Redireciona para a lista de campeonatos

    return render(request, 'deletar_campeonato.html', {'campeonato': campeonato})

