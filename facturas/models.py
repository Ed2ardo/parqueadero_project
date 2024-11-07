from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from tarifas.models import Tarifa
from gestion_parqueadero.models import RegistroParqueo
from clientes.models import Cliente
from decimal import Decimal


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    registro_parqueo = models.ForeignKey(
        RegistroParqueo, on_delete=models.CASCADE)
    tarifa = models.ForeignKey(
        Tarifa, on_delete=models.SET_NULL, null=True, blank=True)
    monto = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    tiempo_total = models.DurationField(null=True, blank=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Obtener el registro de parqueo asociado
        registro = self.registro_parqueo

        # Verificar que exista fecha de entrada y salida
        if registro.fecha_entrada and registro.fecha_salida:
            # Calcular el tiempo total
            tiempo_total = registro.fecha_salida - registro.fecha_entrada
            self.tiempo_total = tiempo_total

            # Obtener la tarifa según el tipo de vehículo
            tipo_vehiculo = registro.vehiculo.tipo
            tarifa = Tarifa.objects.filter(tipo_vehiculo=tipo_vehiculo).first()
            if tarifa is None:
                raise ValidationError(
                    "No se encontró una tarifa para el tipo de vehículo especificado.")

            self.tarifa = tarifa

            # Calcular el monto
            # Convierte segundos a horas como Decimal
            horas_estacionadas = Decimal(
                tiempo_total.total_seconds()) / Decimal(3600)
            self.monto = tarifa.costo_por_hora * horas_estacionadas
        else:
            raise ValidationError(
                "El registro de parqueo debe tener fechas de entrada y salida para calcular la factura.")

        # Llamar al método save original para guardar la factura
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura de {self.cliente} para el registro {self.registro_parqueo}"
