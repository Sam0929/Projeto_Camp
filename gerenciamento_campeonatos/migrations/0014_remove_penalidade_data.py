# Generated by Django 5.1.3 on 2024-11-13 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento_campeonatos', '0013_remove_penalidadeeliminatoria_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='penalidade',
            name='data',
        ),
    ]