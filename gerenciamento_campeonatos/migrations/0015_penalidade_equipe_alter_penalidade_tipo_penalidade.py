# Generated by Django 5.1.3 on 2024-11-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento_campeonatos', '0014_remove_penalidade_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='penalidade',
            name='equipe',
            field=models.CharField(blank=True, choices=[('participante', 'Por Participante'), ('casa', 'Equipe Casa'), ('fora', 'Equipe Fora')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='penalidade',
            name='tipo_penalidade',
            field=models.CharField(blank=True, choices=[('amarelo', 'Cartão Amarelo'), ('vermelho', 'Cartão Vermelho'), ('expulsao', 'Expulsão'), ('outro', 'Outro')], max_length=50, null=True),
        ),
    ]