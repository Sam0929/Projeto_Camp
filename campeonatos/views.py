from django.shortcuts import render, get_object_or_404, redirect
from .models import Campeonato, Inscricao
from .forms import CampeonatoForm, InscricaoForm
from django.contrib import messages
from django.utils import timezone
from collections import defaultdict

def campeonatos(request):
    campeonatos = Campeonato.objects.all()
    
    # Para cada campeonato, agrupamos os participantes por equipe
    for campeonato in campeonatos:
        # Cria um dicionário onde a chave será a equipe (normalizada) e o valor será uma lista de participantes
        equipes_participantes = defaultdict(list)
        for inscricao in campeonato.inscricao_set.all():
            # Normaliza o nome da equipe (sem espaços extras e com letras minúsculas)
            equipe_normalizada = inscricao.equipe_participante.strip().lower()
            equipes_participantes[equipe_normalizada].append(inscricao)
        
        # Anexa o dicionário ao objeto campeonato para ser usado no template
        campeonato.equipes_participantes = equipes_participantes

    return render(request, 'campeonatos.html', {'campeonatos': campeonatos})

def criar_campeonato(request):
    if request.method == 'POST':
        print("Dados recebidos:", request.POST)  # Debug
        form = CampeonatoForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            hoje = timezone.now()  # timezone.now() retorna datetime com data e hora
            
            if data_inicio < hoje:
                form.add_error('data_inicio', 'A data de início não pode ser no passado.')
            else:
                campeonato = form.save(commit=False)
                campeonato.save()
                form.save_m2m()  # Salva as relações ManyToMany, se houver
                return redirect('campeonatos')  # Redireciona para a lista de campeonatos
    else:
        form = CampeonatoForm()

    return render(request, 'criar_campeonato.html', {'form': form})

def editar_campeonato(request, pk):
    campeonato = get_object_or_404(Campeonato, pk=pk)
    if request.method == 'POST':
        form = CampeonatoForm(request.POST, instance=campeonato)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            hoje = timezone.now()

            if data_inicio < hoje:
                form.add_error('data_inicio', 'A data de início não pode ser no passado.')
            elif data_fim <= data_inicio:
                form.add_error('data_fim', 'A data de fim deve ser posterior à data de início.')
            else:
                form.save()
                return redirect('campeonatos')
    else:
        form = CampeonatoForm(instance=campeonato)
    
    # Passa também os participantes (inscritos) para o template
    participantes = campeonato.inscricao_set.all()

    return render(request, 'editar_campeonato.html', {
        'form': form,
        'campeonato': campeonato,
        'participantes': participantes,
    })

def deletar_campeonato(request, pk):
    campeonato = get_object_or_404(Campeonato, pk=pk)
    if request.method == 'POST':
        campeonato.delete()
        return redirect('campeonatos')

    return render(request, 'deletar_campeonato.html', {'campeonato': campeonato})

def inscrever_participante(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)

    # Verificar se o campeonato já atingiu o número máximo de participantes
    if campeonato.inscricao_set.count() >= campeonato.numero_maximo_participantes:
        return render(request, 'campeonato_lotado.html', {'campeonato': campeonato})
    
    if request.method == 'POST':
        nome_participante = request.POST['nome_participante']
        email_participante = request.POST['email_participante']
        equipe_participante = request.POST['equipe_participante']
        
        # Criar a inscrição
        Inscricao.objects.create(
            campeonato=campeonato,
            nome_participante=nome_participante,
            email_participante=email_participante,
            equipe_participante=equipe_participante
        )
        
        return redirect('campeonatos')

    return render(request, 'inscricao.html', {'campeonato': campeonato})

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
            return redirect('campeonatos')
    else:
        form = InscricaoForm(instance=participante)

    return render(request, 'editar_participante.html', {'form': form, 'participante': participante})
