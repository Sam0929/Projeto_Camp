from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria um usuário admin caso não exista'

    def handle(self, *args, **kwargs):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'

        # Verifica se o usuário admin já existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'O usuário admin já existe.'))
        else:
            # Cria o usuário admin
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Usuário admin criado com sucesso.'))
