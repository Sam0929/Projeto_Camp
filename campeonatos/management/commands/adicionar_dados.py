from django.core.management.base import BaseCommand
from campeonatos.models import Campeonato, Participante

class Command(BaseCommand):
    help = 'Adiciona dados de teste ao sistema de campeonatos'

    def handle(self, *args, **kwargs):
        if not Campeonato.objects.exists():
            self.stdout.write('Adicionando dados de teste...')

            # Lista de dados de campeonatos
            campeonatos_data = [
                {
                    'nome': 'Campeonato de Teste 1',
                    'data_inicio': '2024-01-01',
                    'data_fim': '2024-01-10',
                    'descricao': 'Este é o primeiro campeonato de teste.',
                    'premiação': 1000.00,
                    'participantes': [
                        {'nome': 'João Silva', 'email': 'joao@example.com', 'equipe': 'Equipe A'},
                        {'nome': 'Maria Oliveira', 'email': 'maria@example.com', 'equipe': 'Equipe B'},
                    ]
                },
                {
                    'nome': 'Campeonato de Teste 2',
                    'data_inicio': '2024-02-01',
                    'data_fim': '2024-02-10',
                    'descricao': 'Este é o segundo campeonato de teste.',
                    'premiação': 2000.00,
                    'participantes': [
                        {'nome': 'Carlos Pereira', 'email': 'carlos@example.com', 'equipe': 'Equipe C'},
                        {'nome': 'Ana Costa', 'email': 'ana@example.com', 'equipe': 'Equipe D'},
                    ]
                },
                {
                    'nome': 'Campeonato de Teste 3',
                    'data_inicio': '2024-03-01',
                    'data_fim': '2024-03-10',
                    'descricao': 'Este é o terceiro campeonato de teste.',
                    'premiação': 1500.00,
                    'participantes': [
                        {'nome': 'Pedro Lima', 'email': 'pedro@example.com', 'equipe': 'Equipe E'},
                        {'nome': 'Lucas Martins', 'email': 'lucas@example.com', 'equipe': 'Equipe F'},
                    ]
                },
            ]

            for data in campeonatos_data:
                # Criando o campeonato
                campeonato = Campeonato.objects.create(
                    nome=data['nome'],
                    data_inicio=data['data_inicio'],
                    data_fim=data['data_fim'],
                    descricao=data['descricao'],
                    premiação=data['premiação']
                )

                # Criando e adicionando participantes
                for participante_data in data['participantes']:
                    participante = Participante.objects.create(**participante_data)
                    campeonato.participantes.add(participante)

            self.stdout.write(self.style.SUCCESS('Dados de teste adicionados com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Campeonatos já existem no banco de dados. Nenhum dado foi adicionado.'))
