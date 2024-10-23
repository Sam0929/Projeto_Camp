import random
from django.core.management.base import BaseCommand
from campeonatos.models import Campeonato, Participante, Inscricao
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = 'Adiciona dados de teste com participantes aleatórios ao sistema de campeonatos'

    def handle(self, *args, **kwargs):
        if not Campeonato.objects.exists():
            self.stdout.write('Adicionando dados de teste...')

            # Lista de participantes fornecida
            participantes_data = [
                {'nome_participante': 'Alexandre Augusto Tescaro Oliveira', 'email_participante': 'alexandre.tescaro@gmail.com'},
                {'nome_participante': 'André Pádua da Costa', 'email_participante': 'andrepadua@gmail.com'},
                {'nome_participante': 'Angelo Geraldo Pereira Junior', 'email_participante': 'angelopereira@gmail.com'},
                {'nome_participante': 'Augusto Guaschi Morato', 'email_participante': 'augusto.morato@gmail.com'},
                {'nome_participante': 'Beatriz Cupa Newman', 'email_participante': 'beatriz.newman@gmail.com'},
                {'nome_participante': 'Daniel Scanavini Rossi', 'email_participante': 'daniel.rossi@gmail.com'},
                {'nome_participante': 'Daniela Akemi Hayashi', 'email_participante': 'daniela.hayashi@gmail.com'},
                {'nome_participante': 'Eduardo da Silva dos Santos', 'email_participante': 'eduardo.santos@gmail.com'},
                {'nome_participante': 'Eduardo de Faria Rios Perucello', 'email_participante': 'eduardo.perucello@gmail.com'},
                {'nome_participante': 'Enzo Cesar Consulo Silva', 'email_participante': 'enzoconsulo@gmail.com'},
                {'nome_participante': 'Enzo Fabrício Monteiro Correia de Souza', 'email_participante': 'enzomonteiro@gmail.com'},
                {'nome_participante': 'Felipe Dias Konda', 'email_participante': 'felipe.konda@gmail.com'},
                {'nome_participante': 'Flávia Cristina Medeiros', 'email_participante': 'flavia.medeiros@gmail.com'},
                {'nome_participante': 'Gabriel de Toledo Lopes', 'email_participante': 'gabriel.lopes@gmail.com'},
                {'nome_participante': 'Gabriel Hideki Yamamoto', 'email_participante': 'gabriel.yamamoto@gmail.com'},
                {'nome_participante': 'Giovana Salazar Alarcon', 'email_participante': 'giovana.alarcon@gmail.com'},
                {'nome_participante': 'Giovani Bellini dos Santos', 'email_participante': 'giovani.bellini@gmail.com'},
                {'nome_participante': 'Gonzalo Gontijo Veloso Teixeira Roque', 'email_participante': 'gonzalo.teixeira@gmail.com'},
                {'nome_participante': 'Guilherme Bernardini Roelli', 'email_participante': 'guilherme.roelli@gmail.com'},
                {'nome_participante': 'Guilherme Lopes Silva', 'email_participante': 'guilhermelopes@gmail.com'},
                {'nome_participante': 'Hugo Tahara Menegatti', 'email_participante': 'hugo.menegatti@gmail.com'},
                {'nome_participante': 'João Pedro Bierenbach Souza Camargo', 'email_participante': 'joao.bierenbach@gmail.com'},
                {'nome_participante': 'João Victor Vasconcelos Junqueira Criscuolo', 'email_participante': 'joaovicto.criscuolo@gmail.com'},
                {'nome_participante': 'Joao Vitor Ferreira dos Santos', 'email_participante': 'joaovitor.santos@gmail.com'},
                {'nome_participante': 'Jose Pascoal Martins', 'email_participante': 'jose.martins@gmail.com'},
                {'nome_participante': 'Júlia Machado Duran', 'email_participante': 'julia.duran@gmail.com'},
                {'nome_participante': 'Kauai Duhamel Buranello', 'email_participante': 'kauai.buranello@gmail.com'},
                {'nome_participante': 'Larry Luiz Alves Filho', 'email_participante': 'larry.alves@gmail.com'},
                {'nome_participante': 'Leonardo Caberlim de Souza', 'email_participante': 'leonardo.souza@gmail.com'},
                {'nome_participante': 'Leonardo Seiji Kaetsu', 'email_participante': 'leonardo.kaetsu@gmail.com'},
                {'nome_participante': 'Luana Bresciani Baptista', 'email_participante': 'luana.baptista@gmail.com'},
                {'nome_participante': 'Lucas Magaldi', 'email_participante': 'lucas.magaldi@gmail.com'},
                {'nome_participante': 'Lucas Pegoraro Marzochi', 'email_participante': 'lucas.marzochi@gmail.com'},
                {'nome_participante': 'Lucas Valério Berti', 'email_participante': 'lucas.berti@gmail.com'},
                {'nome_participante': 'Lucca Vasconcelos Costa Oliveira', 'email_participante': 'lucca.oliveira@gmail.com'},
                {'nome_participante': 'Luigi Bertoli Menezes', 'email_participante': 'luigi.menezes@gmail.com'},
                {'nome_participante': 'Luis Felipe Cintra Braga', 'email_participante': 'luis.braga@gmail.com'},
                {'nome_participante': 'Luís Guilherme Pilotto de Menezes Rego', 'email_participante': 'luis.rego@gmail.com'},
                {'nome_participante': 'Maiza Leticia Oliveira', 'email_participante': 'maiza.oliveira@gmail.com'},
                {'nome_participante': 'Mateus Navarro Bella Cruz', 'email_participante': 'mateus.cruz@gmail.com'},
                {'nome_participante': 'Matheus Ecke Medeiros', 'email_participante': 'matheus.medeiros@gmail.com'},
                {'nome_participante': 'Matheus Gonçalves Anitelli', 'email_participante': 'matheus.anitelli@gmail.com'},
                {'nome_participante': 'Mauricio Lasca Gonçales', 'email_participante': 'mauricio.goncalves@gmail.com'},
                {'nome_participante': 'Murilo Alves Croce', 'email_participante': 'murilo.croce@gmail.com'},
                {'nome_participante': 'Murilo Montebello', 'email_participante': 'murilo.montebello@gmail.com'},
                {'nome_participante': 'Nathan Gonzalez Jurcevic', 'email_participante': 'nathan.jurcevic@gmail.com'},
                {'nome_participante': 'Pedro Augusto Eickhoff', 'email_participante': 'pedro.eickhoff@gmail.com'},
                {'nome_participante': 'Pedro Fernandes Di Grazia', 'email_participante': 'pedro.grazia@gmail.com'},
                {'nome_participante': 'Pedro Henrique Ribeiro Pistarini', 'email_participante': 'pedroribeiro@gmail.com'},
                {'nome_participante': 'Pedro Rodolfo da Silva Galvão Santos', 'email_participante': 'pedrogalvao@gmail.com'},
                {'nome_participante': 'Rafael Mazolini Fernandes', 'email_participante': 'rafael.mazolini@gmail.com'},
                {'nome_participante': 'Renan Rohers Salvador', 'email_participante': 'renan.salvador@gmail.com'},
                {'nome_participante': 'Samuel Vanini', 'email_participante': 'samuel.vanini@gmail.com'},
                {'nome_participante': 'Taynara Araujo de Assis', 'email_participante': 'taynara.assis@gmail.com'},
                {'nome_participante': 'Tiago Oliveira Dallécio', 'email_participante': 'tiago.dallecio@gmail.com'},
                {'nome_participante': 'Victor de Melo Roston', 'email_participante': 'victor.roston@gmail.com'},
                {'nome_participante': 'Vinícius Afonso Alvarez', 'email_participante': 'vinicius.alvarez@gmail.com'},
                {'nome_participante': 'Vinícius Barbosa de Souza', 'email_participante': 'vinicius.barbosa@gmail.com'},
                {'nome_participante': 'Vinícius Borges de Godoy', 'email_participante': 'vinicius.godoy@gmail.com'},
                {'nome_participante': 'Vinicius Felippe Dan Albieri', 'email_participante': 'vinicius.albieri@gmail.com'},
                {'nome_participante': 'Vinicius Hardy Barros', 'email_participante': 'vinicius.barros@gmail.com'},
                {'nome_participante': 'Vinicius Henrique Galassi', 'email_participante': 'vinicius.galassi@gmail.com'},
                {'nome_participante': 'Vitor Yuzo Takei', 'email_participante': 'vitor.takei@gmail.com'},
                {'nome_participante': 'Yan Shinji Nagata Shinohara', 'email_participante': 'yan.shinohara@gmail.com'}
            ]

            # Função para criar participantes e inscrições
            def criar_participante(nome, email, equipe, campeonato):
                participante, created = Participante.objects.get_or_create(
                    nome_participante=nome,
                    email_participante=email,
                    equipe_participante=equipe,
                    campeonato=campeonato
                )
                Inscricao.objects.create(campeonato=campeonato, participante=participante)
                return participante

            # Criar Campeonato de Beach Tennis (10 equipes com 2 participantes cada)
            campeonato_beach_tennis = Campeonato.objects.create(
                nome='Campeonato de Beach Tennis',
                data_inicio=timezone.make_aware(datetime.strptime('2024-11-01 19:00', '%Y-%m-%d %H:%M')),
                data_fim=timezone.make_aware(datetime.strptime('2024-12-30 23:00', '%Y-%m-%d %H:%M')),
                descricao='Campeonato de Beach Tennis',
                premiação=1000.00,
                numero_maximo_participantes=20
            )
            random.shuffle(participantes_data)
            for i in range(0, 20, 2):
                equipe = f"Equipe Beach {i//2 + 1}"
                criar_participante(participantes_data[i]['nome_participante'], participantes_data[i]['email_participante'], equipe, campeonato_beach_tennis)
                criar_participante(participantes_data[i+1]['nome_participante'], participantes_data[i+1]['email_participante'], equipe, campeonato_beach_tennis)

            # Criar Campeonato de Futebol (6 equipes com 10 participantes cada)
            campeonato_futebol = Campeonato.objects.create(
                nome='Campeonato de Futebol',
                data_inicio=timezone.make_aware(datetime.strptime('2024-11-01 18:00', '%Y-%m-%d %H:%M')),
                data_fim=timezone.make_aware(datetime.strptime('2025-02-20 23:00', '%Y-%m-%d %H:%M')),
                descricao='Campeonato de Futebol',
                premiação=5000.00,
                numero_maximo_participantes=60
            )
            random.shuffle(participantes_data)
            for i in range(0, 60, 10):
                equipe = f"Equipe Futebol {i//10 + 1}"
                for j in range(10):
                    criar_participante(participantes_data[i+j]['nome_participante'], participantes_data[i+j]['email_participante'], equipe, campeonato_futebol)

            # Criar Campeonato de Xadrez (16 equipes com 1 participante cada)
            campeonato_xadrez = Campeonato.objects.create(
                nome='Campeonato de Xadrez',
                data_inicio=timezone.make_aware(datetime.strptime('2024-12-01 10:00', '%Y-%m-%d %H:%M')),
                data_fim=timezone.make_aware(datetime.strptime('2024-12-30 20:00', '%Y-%m-%d %H:%M')),
                descricao='Campeonato de Xadrez',
                premiação=1500.00,
                numero_maximo_participantes=16
            )
            random.shuffle(participantes_data)
            for i in range(16):
                equipe = f"Equipe Xadrez {i + 1}"
                criar_participante(participantes_data[i]['nome_participante'], participantes_data[i]['email_participante'], equipe, campeonato_xadrez)

            self.stdout.write(self.style.SUCCESS('Dados de teste adicionados com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Campeonatos já existem no banco de dados. Nenhum dado foi adicionado.'))
