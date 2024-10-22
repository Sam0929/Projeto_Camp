from django.core.management.base import BaseCommand
from campeonatos.models import Campeonato, Participante, Inscricao
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = 'Adiciona dados de teste ao sistema de campeonatos'

    def handle(self, *args, **kwargs):
        if not Campeonato.objects.exists():
            self.stdout.write('Adicionando dados de teste...')

            campeonatos_data = [
                {
                    'nome': 'Campeonato de Teste 1',
                    'data_inicio': '2024-01-01',
                    'data_fim': '2024-01-10',
                    'descricao': 'Este é o primeiro campeonato de teste.',
                    'participantes': [
                        {'nome': 'João Silva', 'email': 'joao@example.com', 'equipe': 'Equipe A'},
                        {'nome': 'Maria Oliveira', 'email': 'maria@example.com', 'equipe': 'Equipe A'},
                        {'nome': 'Carlos Pereira', 'email': 'carlos@example.com', 'equipe': 'Equipe B'},
                        {'nome': 'Ana Costa', 'email': 'ana@example.com', 'equipe': 'Equipe B'}
                    ],
                    'premiação': 2000.00,
                    'numero_maximo_participantes': 10,
                },
                {
                    'nome': 'Campeonato de Teste 2',
                    'data_inicio': '2024-02-01',
                    'data_fim': '2024-02-10',
                    'descricao': 'Este é o segundo campeonato de teste.',
                    'participantes': [
                        {'nome': 'Lucas Souza', 'email': 'lucas@example.com', 'equipe': 'Equipe C'},
                        {'nome': 'Juliana Souza', 'email': 'juliana@example.com', 'equipe': 'Equipe C'},
                        {'nome': 'Fernanda Lima', 'email': 'fernanda@example.com', 'equipe': 'Equipe D'},
                        {'nome': 'Paulo Alves', 'email': 'paulo@example.com', 'equipe': 'Equipe D'}
                    ],
                    'premiação': 3000.00,
                    'numero_maximo_participantes': 10,
                },
                {
                    'nome': 'Campeonato de Teste 3',
                    'data_inicio': '2024-03-01',
                    'data_fim': '2024-03-10',
                    'descricao': 'Este é o terceiro campeonato de teste.',
                    'participantes': [
                        {'nome': 'Pedro Lima', 'email': 'pedro@example.com', 'equipe': 'Equipe E'},
                        {'nome': 'Lucas Martins', 'email': 'lucas@example.com', 'equipe': 'Equipe E'},
                        {'nome': 'Gabriel Mendes', 'email': 'gabriel@example.com', 'equipe': 'Equipe F'},
                        {'nome': 'Rafael Souza', 'email': 'rafael@example.com', 'equipe': 'Equipe F'}
                    ],
                    'premiação': 1000.00,
                    'numero_maximo_participantes': 10,
                },
            ]

            for data in campeonatos_data:
                # Criando o campeonato
                campeonato = Campeonato.objects.create(
                    nome=data['nome'],
                    data_inicio=timezone.make_aware(datetime.strptime(data['data_inicio'], '%Y-%m-%d')),
                    data_fim=timezone.make_aware(datetime.strptime(data['data_fim'], '%Y-%m-%d')),
                    descricao=data['descricao'],
                    premiação=data['premiação']
                )

                # Criando e adicionando participantes
                for participante_data in data['participantes']:
                    participante, created = Participante.objects.get_or_create(
                        nome=participante_data['nome'],
                        email=participante_data['email'],
                        equipe=participante_data['equipe'],
                        campeonato=campeonato
                    )

                    # Criando a inscrição
                    Inscricao.objects.create(
                        campeonato=campeonato,
                        participante=participante
                    )

            self.stdout.write(self.style.SUCCESS('Dados de teste adicionados com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Campeonatos já existem no banco de dados. Nenhum dado foi adicionado.'))
