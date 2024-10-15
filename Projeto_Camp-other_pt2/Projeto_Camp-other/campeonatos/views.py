from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Campeonato, Inscricao
from .forms import CampeonatoForm, InscricaoForm
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
    
    # Passa também os participantes (inscritos) para o template
    participantes = campeonato.inscricao_set.all()  # Acessa o related_name da ForeignKey

    return render(request, 'editar_campeonato.html', {
        'form': form,
        'campeonato': campeonato,
        'participantes': participantes,  # Passa os participantes
    })

def deletar_campeonato(request, pk):
    campeonato = get_object_or_404(Campeonato, pk=pk)
    if request.method == 'POST':
        campeonato.delete()
        return redirect('campeonatos')  # Redireciona para a lista de campeonatos

    return render(request, 'deletar_campeonato.html', {'campeonato': campeonato})

def inscrever_participante(request, pk):
    campeonato = get_object_or_404(Campeonato, pk=pk)
    
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.campeonato = campeonato  # Liga a inscrição ao campeonato específico
            inscricao.save()
            messages.success(request, 'Inscrição realizada com sucesso!')
            return redirect('campeonatos')  # Redireciona para a lista de campeonatos
        else:
            messages.error(request, 'Erro na inscrição. Verifique os dados fornecidos.')
    else:
        form = InscricaoForm()

    return render(request, 'inscricao.html', {'form': form, 'campeonato': campeonato})

def excluir_participante(request, pk):
    participante = get_object_or_404(Inscricao, pk=pk)
    
    if request.method == 'POST':
        participante.delete()
        return redirect('editar_campeonato', pk=participante.campeonato.pk)
    
    return redirect('editar_campeonato', pk=participante.campeonato.pk)

def editar_participante(request, pk):
    participante = get_object_or_404(Inscricao, pk=pk)
    if request.method == 'POST':
        form = InscricaoForm(request.POST, instance=participante)
        if form.is_valid():
            form.save()
            return redirect('campeonatos')  # Ou redirecionar para onde preferir
    else:
        form = InscricaoForm(instance=participante)

    return render(request, 'editar_participante.html', {'form': form, 'participante': participante})
