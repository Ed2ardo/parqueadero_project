# Generated by Django 5.1.2 on 2024-11-28 13:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='El teléfono debe contener exactamente 10 dígitos.', regex='^/d{10}$')]),
        ),
    ]
