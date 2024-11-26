from django.shortcuts import render, get_object_or_404, redirect
from .models import Campeonato, Inscricao
from .forms import CampeonatoForm, InscricaoForm
from django.contrib import messages
from django.utils import timezone
from collections import defaultdict
from .models import Participante
from .forms import ParticipanteForm
from django.db import connection
from sistema_campeonatos.middleware import admin_required
from django.contrib.auth.decorators import login_required


from django.db.models import Q

def campeonatos(request):
    query = request.GET.get('q', '')  # Pesquisa por texto
    data_inicio = request.GET.get('data_inicio')  # Filtro por data de início
    campeonatos = Campeonato.objects.all()
    
    # Filtro por texto
    if query:
        campeonatos = campeonatos.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        )
    
    # Filtro por data de início
    if data_inicio:
        campeonatos = campeonatos.filter(data_inicio__date=data_inicio)
    
    return render(request, 'campeonatos.html', {'campeonatos': campeonatos, 'query': query})



def criar_campeonato(request):
    if request.method == 'POST':
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

@admin_required
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
    
    # Pegar os participantes relacionados ao campeonato via o modelo Inscricao
    inscricoes = campeonato.inscricao_set.all()

    return render(request, 'editar_campeonato.html', {
        'form': form,
        'campeonato': campeonato,
        'inscricoes': inscricoes,  # Passa as inscrições para o template
    })

@admin_required
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
        messages.error(request, 'O campeonato já atingiu o número máximo de participantes.')
        return render(request, 'inscricao.html', {'campeonato': campeonato, 'form': InscricaoForm()})

    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            participante = form.cleaned_data['participante']

            if Inscricao.objects.filter(campeonato=campeonato, participante=participante).exists():
                messages.error(request, 'Este participante já está inscrito no campeonato.')
            else:
                Inscricao.objects.create(campeonato=campeonato, participante=participante)
                return redirect('campeonatos')  # Redireciona após a inscrição

    else:
        form = InscricaoForm()

    return render(request, 'inscricao.html', {'campeonato': campeonato, 'form': form})


@admin_required
def excluir_participante(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    
    if request.method == 'POST':
        campeonato_id = inscricao.campeonato.pk  # Salva o ID do campeonato antes de excluir
        inscricao.delete()  # Exclui a inscrição

        # Remoção da lógica de renumeração de IDs - não é necessário e não recomendado
        # O banco de dados deve gerenciar os IDs automaticamente

        return redirect('editar_campeonato', pk=campeonato_id)

    # Redireciona de volta para a página de edição do campeonato, mesmo que o método não seja POST
    return redirect('editar_campeonato', pk=inscricao.campeonato.pk)


@admin_required
def editar_participante(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)  # Pega a inscrição
    participante = inscricao.participante  # Obtém o participante associado

    if request.method == 'POST':
        form = ParticipanteForm(request.POST, instance=participante)  # Usar ParticipanteForm
        if form.is_valid():
            form.save()
            messages.success(request, 'Participante atualizado com sucesso!')
            return redirect('editar_campeonato', pk=inscricao.campeonato.pk)  # Redireciona para o campeonato
    else:
        form = ParticipanteForm(instance=participante)  # Preenche o formulário com os dados do participante

    return render(request, 'editar_participante.html', {'form': form, 'participante': participante})

@login_required
def novo_participante(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)

    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.campeonato = campeonato
            participante.save()
            return redirect('inscrever_participante', campeonato_id=campeonato_id)
    else:
        form = ParticipanteForm()

    return render(request, 'novo_participante.html', {
        'form': form,
        'campeonato': campeonato,
        'user': request.user,  # Passa os dados do usuário logado
    })
