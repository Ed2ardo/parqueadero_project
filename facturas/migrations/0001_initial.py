# Generated by Django 5.1.2 on 2024-11-28 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
        ('gestion_parqueadero', '0001_initial'),
        ('tarifas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tiempo_total', models.DurationField(blank=True, null=True)),
                ('fecha_emision', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
                ('registro_parqueo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_parqueadero.registroparqueo')),
                ('tarifa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tarifas.tarifa')),
            ],
        ),
    ]
