from django.db import models
from clientes.models import Cliente
from gestion_parqueadero.models import RegistroParqueo
from tarifas.models import Tarifa

# facturas models:


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    registro_parqueo = models.ForeignKey(
        RegistroParqueo, on_delete=models.CASCADE)
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_total = models.DurationField()
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura {self.id} - cliente: {self.cliente.nombre} - Monto: {self.monto}"
