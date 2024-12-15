from django.db import models
from usuarios.models import Usuario
from clientes.models import Cliente
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal


# Configuración de espacios por tipo de vehículo
class EspacioParqueoConfig(models.Model):
    TIPO_ESPACIO_CHOICES = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('bici', 'Bicicleta'),
        ('otros', 'Otros')
    ]

    tipo_espacio = models.CharField(
        max_length=10, choices=TIPO_ESPACIO_CHOICES, unique=True
    )
    total_espacios = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name="Total de Espacios"
    )
    espacios_ocupados = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Espacios Ocupados"
    )

    def clean(self):
        if self.espacios_ocupados > self.total_espacios:
            raise ValidationError(
                "Los espacios ocupados no pueden exceder el total de espacios.")

    def __str__(self):
        return f"{self.get_tipo_espacio_display()} - Total Espacios: {self.total_espacios}"

    class Meta:
        verbose_name = "Configuración de Espacio de Parqueo"
        verbose_name_plural = "Configuraciones de Espacios de Parqueo"


# Modelo para los vehículos
class Vehiculo(models.Model):
    TIPO_VEHICULO_CHOICES = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('bici', 'Bicicleta'),
        ('otros', 'Otros')
    ]

    placa = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(
            regex='^[A-Z0-9-]{6,10}$',
            message='Formato de placa inválido (solo mayúsculas, números y guiones).'
        )],
        verbose_name="Placa del Vehículo"
    )
    tipo = models.CharField(
        max_length=10, choices=TIPO_VEHICULO_CHOICES, verbose_name="Tipo de Vehículo"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vehiculos",
        verbose_name="Cliente Asociado"
    )

    def clean(self):
        if not self.placa and self.tipo != 'bici':
            raise ValidationError("Solo las bicicletas pueden no tener placa.")
        if self.tipo not in dict(self.TIPO_VEHICULO_CHOICES):
            raise ValidationError("El tipo de vehículo no es válido.")

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.placa if self.placa else 'Sin Placa'}"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"


# Registro de entradas y salidas
class RegistroParqueo(models.Model):
    ESTADO_CHOICES = [
        ("activo", "Activo"),
        ("baja", "Baja"),
        ("facturado", "Facturado"),
    ]

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name="registros_parqueo",
        verbose_name="Vehículo Asociado"
    )
    usuario_registra = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registros_registrados",
        verbose_name="Usuario que Registró"
    )
    fecha_entrada = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha y Hora de Entrada"
    )
    fecha_salida = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha y Hora de Salida"
    )
    tiempo_estacionado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Tiempo Estacionado (en minutos)"
    )
    total_cobro = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Total Cobrado")

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="activo",
        verbose_name="Estado del Registro"
    )

    def clean(self):
        if RegistroParqueo.objects.filter(vehiculo=self.vehiculo, estado="activo").exclude(id=self.id).exists():
            raise ValidationError("Este vehículo ya tiene un registro activo.")

    def save(self, *args, **kwargs):
        if self.fecha_salida and self.fecha_entrada:
            delta = self.fecha_salida - self.fecha_entrada
            self.tiempo_estacionado = Decimal(
                delta.total_seconds()) / 60  # Minutos
            tarifa = Tarifa.objects.filter(
                tipo_vehiculo=self.vehiculo.tipo).first()
            if tarifa:
                self.total_cobro = self.tiempo_estacionado * tarifa.costo_por_minuto
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Registro {self.vehiculo.placa} - Entrada: {self.fecha_entrada} - Salida: {self.fecha_salida}"

    class Meta:
        verbose_name = "Registro de Parqueo"
        verbose_name_plural = "Registros de Parqueo"


class Tarifa(models.Model):
    TIPO_VEHICULO_CHOICES = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('bici', 'Bicicleta'),
        ('otros', 'Otros')
    ]
    tipo_vehiculo = models.CharField(
        max_length=10, choices=TIPO_VEHICULO_CHOICES
    )
    costo_por_minuto = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Costo por minuto"
    )

    def clean(self):
        if self.costo_por_minuto <= 0:
            raise ValidationError(
                "El costo por minuto debe ser mayor a 0."
            )

    def __str__(self):
        return f"{self.get_tipo_vehiculo_display()} - ${self.costo_por_minuto} por minuto."

    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
