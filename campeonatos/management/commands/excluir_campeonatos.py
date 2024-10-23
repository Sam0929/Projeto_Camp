from django.core.management.base import BaseCommand
from campeonatos.models import Campeonato

class Command(BaseCommand):
    help = 'Exclui todos os campeonatos existentes no banco de dados'

    def handle(self, *args, **kwargs):
        campeonatos = Campeonato.objects.all()
        if campeonatos.exists():
            count = campeonatos.count()
            campeonatos.delete()
            self.stdout.write(self.style.SUCCESS(f'{count} campeonatos foram excluídos com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Nenhum campeonato encontrado no banco de dados.'))