# Generated by Django 5.1.2 on 2024-11-05 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campeonatos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campeonato',
            old_name='premiação',
            new_name='premiacao',
        ),
        migrations.AddField(
            model_name='campeonato',
            name='classificacao_gerada',
            field=models.BooleanField(default=False),
        ),
    ]
