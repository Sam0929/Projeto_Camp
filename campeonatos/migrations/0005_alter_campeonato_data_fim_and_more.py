# Generated by Django 5.1.2 on 2024-10-16 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campeonatos', '0004_campeonato_numero_maximo_participantes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campeonato',
            name='data_fim',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='campeonato',
            name='data_inicio',
            field=models.DateTimeField(),
        ),
    ]