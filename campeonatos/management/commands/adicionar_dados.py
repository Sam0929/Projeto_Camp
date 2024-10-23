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
                {'nome': 'Alexandre Augusto Tescaro Oliveira', 'email': 'alexandre.tescaro@gmail.com'},
                {'nome': 'André Pádua da Costa', 'email': 'andrepadua@gmail.com'},
                {'nome': 'Angelo Geraldo Pereira Junior', 'email': 'angelopereira@gmail.com'},
                {'nome': 'Augusto Guaschi Morato', 'email': 'augusto.morato@gmail.com'},
                {'nome': 'Beatriz Cupa Newman', 'email': 'beatriz.newman@gmail.com'},
                {'nome': 'Daniel Scanavini Rossi', 'email': 'daniel.rossi@gmail.com'},
                {'nome': 'Daniela Akemi Hayashi', 'email': 'daniela.hayashi@gmail.com'},
                {'nome': 'Eduardo da Silva dos Santos', 'email': 'eduardo.santos@gmail.com'},
                {'nome': 'Eduardo de Faria Rios Perucello', 'email': 'eduardo.perucello@gmail.com'},
                {'nome': 'Enzo Cesar Consulo Silva', 'email': 'enzoconsulo@gmail.com'},
                {'nome': 'Enzo Fabrício Monteiro Correia de Souza', 'email': 'enzomonteiro@gmail.com'},
                {'nome': 'Felipe Dias Konda', 'email': 'felipe.konda@gmail.com'},
                {'nome': 'Flávia Cristina Medeiros', 'email': 'flavia.medeiros@gmail.com'},
                {'nome': 'Gabriel de Toledo Lopes', 'email': 'gabriel.lopes@gmail.com'},
                {'nome': 'Gabriel Hideki Yamamoto', 'email': 'gabriel.yamamoto@gmail.com'},
                {'nome': 'Giovana Salazar Alarcon', 'email': 'giovana.alarcon@gmail.com'},
                {'nome': 'Giovani Bellini dos Santos', 'email': 'giovani.bellini@gmail.com'},
                {'nome': 'Gonzalo Gontijo Veloso Teixeira Roque', 'email': 'gonzalo.teixeira@gmail.com'},
                {'nome': 'Guilherme Bernardini Roelli', 'email': 'guilherme.roelli@gmail.com'},
                {'nome': 'Guilherme Lopes Silva', 'email': 'guilhermelopes@gmail.com'},
                {'nome': 'Hugo Tahara Menegatti', 'email': 'hugo.menegatti@gmail.com'},
                {'nome': 'João Pedro Bierenbach Souza Camargo', 'email': 'joao.bierenbach@gmail.com'},
                {'nome': 'João Victor Vasconcelos Junqueira Criscuolo', 'email': 'joaovicto.criscuolo@gmail.com'},
                {'nome': 'Joao Vitor Ferreira dos Santos', 'email': 'joaovitor.santos@gmail.com'},
                {'nome': 'Jose Pascoal Martins', 'email': 'jose.martins@gmail.com'},
                {'nome': 'Júlia Machado Duran', 'email': 'julia.duran@gmail.com'},
                {'nome': 'Kauai Duhamel Buranello', 'email': 'kauai.buranello@gmail.com'},
                {'nome': 'Larry Luiz Alves Filho', 'email': 'larry.alves@gmail.com'},
                {'nome': 'Leonardo Caberlim de Souza', 'email': 'leonardo.souza@gmail.com'},
                {'nome': 'Leonardo Seiji Kaetsu', 'email': 'leonardo.kaetsu@gmail.com'},
                {'nome': 'Luana Bresciani Baptista', 'email': 'luana.baptista@gmail.com'},
                {'nome': 'Lucas Magaldi', 'email': 'lucas.magaldi@gmail.com'},
                {'nome': 'Lucas Pegoraro Marzochi', 'email': 'lucas.marzochi@gmail.com'},
                {'nome': 'Lucas Valério Berti', 'email': 'lucas.berti@gmail.com'},
                {'nome': 'Lucca Vasconcelos Costa Oliveira', 'email': 'lucca.oliveira@gmail.com'},
                {'nome': 'Luigi Bertoli Menezes', 'email': 'luigi.menezes@gmail.com'},
                {'nome': 'Luis Felipe Cintra Braga', 'email': 'luis.braga@gmail.com'},
                {'nome': 'Luís Guilherme Pilotto de Menezes Rego', 'email': 'luis.rego@gmail.com'},
                {'nome': 'Maiza Leticia Oliveira', 'email': 'maiza.oliveira@gmail.com'},
                {'nome': 'Mateus Navarro Bella Cruz', 'email': 'mateus.cruz@gmail.com'},
                {'nome': 'Matheus Ecke Medeiros', 'email': 'matheus.medeiros@gmail.com'},
                {'nome': 'Matheus Gonçalves Anitelli', 'email': 'matheus.anitelli@gmail.com'},
                {'nome': 'Mauricio Lasca Gonçales', 'email': 'mauricio.goncalves@gmail.com'},
                {'nome': 'Murilo Alves Croce', 'email': 'murilo.croce@gmail.com'},
                {'nome': 'Murilo Montebello', 'email': 'murilo.montebello@gmail.com'},
                {'nome': 'Nathan Gonzalez Jurcevic', 'email': 'nathan.jurcevic@gmail.com'},
                {'nome': 'Pedro Augusto Eickhoff', 'email': 'pedro.eickhoff@gmail.com'},
                {'nome': 'Pedro Fernandes Di Grazia', 'email': 'pedro.grazia@gmail.com'},
                {'nome': 'Pedro Henrique Ribeiro Pistarini', 'email': 'pedroribeiro@gmail.com'},
                {'nome': 'Pedro Rodolfo da Silva Galvão Santos', 'email': 'pedrogalvao@gmail.com'},
                {'nome': 'Rafael Mazolini Fernandes', 'email': 'rafael.mazolini@gmail.com'},
                {'nome': 'Renan Rohers Salvador', 'email': 'renan.salvador@gmail.com'},
                {'nome': 'Samuel Vanini', 'email': 'samuel.vanini@gmail.com'},
                {'nome': 'Taynara Araujo de Assis', 'email': 'taynara.assis@gmail.com'},
                {'nome': 'Tiago Oliveira Dallécio', 'email': 'tiago.dallecio@gmail.com'},
                {'nome': 'Victor de Melo Roston', 'email': 'victor.roston@gmail.com'},
                {'nome': 'Vinícius Afonso Alvarez', 'email': 'vinicius.alvarez@gmail.com'},
                {'nome': 'Vinícius Barbosa de Souza', 'email': 'vinicius.barbosa@gmail.com'},
                {'nome': 'Vinícius Borges de Godoy', 'email': 'vinicius.godoy@gmail.com'},
                {'nome': 'Vinicius Felippe Dan Albieri', 'email': 'vinicius.albieri@gmail.com'},
                {'nome': 'Vinicius Hardy Barros', 'email': 'vinicius.barros@gmail.com'},
                {'nome': 'Vinicius Henrique Galassi', 'email': 'vinicius.galassi@gmail.com'},
                {'nome': 'Vitor Yuzo Takei', 'email': 'vitor.takei@gmail.com'},
                {'nome': 'Yan Shinji Nagata Shinohara', 'email': 'yan.shinohara@gmail.com'}
            ]

            # Função para criar participantes e inscrições
            def criar_participante (nome, email, equipe, campeonato):
                participante, created = Participante.objects.get_or_create(
                    nome=nome,
                    email=email,
                    equipe=equipe,
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
                criar_participante(participantes_data[i]['nome'], participantes_data[i]['email'], equipe, campeonato_beach_tennis)
                criar_participante(participantes_data[i+1]['nome'], participantes_data[i+1]['email'], equipe, campeonato_beach_tennis)

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
                    criar_participante(participantes_data[i+j]['nome'], participantes_data[i+j]['email'], equipe, campeonato_futebol)

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
                criar_participante(participantes_data[i]['nome'], participantes_data[i]['email'], equipe, campeonato_xadrez)

            self.stdout.write(self.style.SUCCESS('Dados de teste adicionados com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Campeonatos já existem no banco de dados. Nenhum dado foi adicionado.'))
