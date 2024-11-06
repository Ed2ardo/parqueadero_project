# Generated by Django 5.1.2 on 2024-11-01 22:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
        ('gestion_parqueadero', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registroparqueo',
            old_name='Vehiculo',
            new_name='vehiculo',
        ),
        migrations.RenameField(
            model_name='vehiculo',
            old_name='espacio_id',
            new_name='espacio',
        ),
        migrations.RemoveField(
            model_name='vehiculo',
            name='cliente_id',
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
        ),
    ]