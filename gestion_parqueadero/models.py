from django.db import models
from usuarios.models import Usuario
from clientes.models import Cliente

# gestion_parqueadero models


class EspacioParqueo(models.Model):
    estado_choices = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('reservado', 'Reservado'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    tipo_espacio_choices = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('camioneta', 'Camioneta'),
        ('bici', 'Bicicleta'),
        ('otro', 'Otro'),
    ]

    numero_espacio = models.IntegerField(unique=True)
    estado = models.CharField(max_length=15, choices=estado_choices)
    tipo_espacio = models.CharField(
        max_length=10, choices=tipo_espacio_choices)

    def __str__(self):
        return f"Espacio {self.numero_espacio} - {self.estado}"


class Vehiculo(models.Model):
    tipo_vehiculo_choices = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('camioneta', 'Camioneta'),
        ('bici', 'Bicicleta'),
        ('otro', 'Otro'),
    ]

    placa = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=10, choices=tipo_vehiculo_choices)
    hora_entrada = models.DateTimeField(auto_now_add=True)
    # hora_salida = models.DateTimeField(null=True, blank=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True)
    espacio = models.ForeignKey(
        EspacioParqueo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.placa}"


class RegistroParqueo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    total_cobro = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Registro {self.vehiculo.placa} - Entrada: {self.fecha_entrada} - Salida: {self.fecha_salida}"
