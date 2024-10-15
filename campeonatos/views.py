from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Campeonato
from .forms import CampeonatoForm
from django.contrib import messages

def campeonatos(request):

    campeonatos = Campeonato.objects.all()

    return render(request, 'campeonatos.html', {'campeonatos': campeonatos})

from django.contrib import messages

def criar_campeonato(request):
    if request.method == 'POST':
        print("Dados recebidos:", request.POST)  # Adicione isso para verificar os dados
        form = CampeonatoForm(request.POST)
        if form.is_valid():
            print("Formulário válido, salvando...")  # Mensagem de depuração
            form.save()
            messages.success(request, 'Campeonato criado com sucesso!')
            return redirect('campeonatos')
        else:
            print("Formulário inválido:", form.errors)  # Mostra os erros do formulário
            messages.error(request, 'Erro ao criar campeonato. Verifique os campos.')
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

