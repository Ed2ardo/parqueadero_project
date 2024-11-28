from django.db import models
from usuarios.models import Usuario
from clientes.models import Cliente
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Configuración de espacios por tipo de vehículo


class EspacioParqueoConfig(models.Model):
    tipo_espacio_choices = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('bici', 'Bicicleta'),
    ]

    tipo_espacio = models.CharField(
        max_length=10, choices=tipo_espacio_choices, unique=True)
    total_espacios = models.IntegerField()

    def clean(self):
        if self.total_espacios < 1:
            raise ValidationError(
                "El número total de espacios debe ser mayor que cero.")

    def __str__(self):
        return f"{self.tipo_espacio} - Total Espacios: {self.total_espacios}"


# Modelo para los vehículos
class Vehiculo(models.Model):
    tipo_vehiculo_choices = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('camioneta', 'Camioneta'),
        ('bici', 'Bicicleta'),
        ('otro', 'Otro'),
    ]

    placa = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(
            regex='^[A-Z0-9-]{6,10}$', message='Formato de placa inválido.')]
    )
    tipo = models.CharField(max_length=10, choices=tipo_vehiculo_choices)
    hora_entrada = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )

    def clean(self):
        if self.tipo not in dict(self.tipo_vehiculo_choices):
            raise ValidationError("El tipo de vehículo no es válido.")

    def __str__(self):
        return f"{self.tipo} - {self.placa}"


# Registro de entradas y salidas
class RegistroParqueo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    total_cobro = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def clean(self):
        if self.fecha_salida and self.fecha_salida <= self.fecha_entrada:
            raise ValidationError(
                "La fecha de salida debe ser posterior a la fecha de entrada.")
        if self.total_cobro is not None and self.total_cobro < 0:
            raise ValidationError("El total cobrado no puede ser negativo.")

    def __str__(self):
        return f"Registro {self.vehiculo.placa} - Entrada: {self.fecha_entrada} - Salida: {self.fecha_salida}"
