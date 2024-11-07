from django.db import models

class Tarifa(models.Model):
    tipo_vehiculo_choices = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('camioneta', 'Camioneta'),
        ('bici', 'Bicicleta'),
        ('otro', 'Otro'),
    ]

    tipo_vehiculo = models.CharField(
        max_length=10, choices=tipo_vehiculo_choices)
    costo_por_hora = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.tipo_vehiculo} - ${self.costo_por_hora} por hora."
