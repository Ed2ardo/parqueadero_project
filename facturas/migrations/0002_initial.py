# Generated by Django 5.1.4 on 2024-12-14 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facturas', '0001_initial'),
        ('gestion_parqueadero', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='registro_parqueo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='factura', to='gestion_parqueadero.registroparqueo', verbose_name='Registro de Parqueo Asociado'),
        ),
    ]
