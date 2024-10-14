from django.core.management.base import BaseCommand
from campeonatos.models import Campeonato, Participante

class Command(BaseCommand):
    help = 'Adiciona dados de teste ao sistema de campeonatos'

    def handle(self, *args, **kwargs):
        if not Campeonato.objects.exists():
            self.stdout.write('Adicionando dados de teste...')
            campeonato = Campeonato.objects.create(
                nome='Campeonato de Teste',
                data_inicio='2024-01-01',
                data_fim='2024-01-10',
                descricao='Este é um campeonato de teste.',
                premiação=1000.00
            )

            # Criando participantes
            participante1 = Participante.objects.create(nome='João Silva', email='joao@example.com', equipe='Equipe A')
            participante2 = Participante.objects.create(nome='Maria Oliveira', email='maria@example.com', equipe='Equipe B')

            # Adicionando participantes ao campeonato
            campeonato.participantes.add(participante1, participante2)

            self.stdout.write(self.style.SUCCESS('Dados de teste adicionados com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Campeonatos já existem no banco de dados. Nenhum dado foi adicionado.'))
