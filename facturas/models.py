from django.db import models
from clientes.models import Cliente
from gestion_parqueadero.models import RegistroParqueo

# facturas models:


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    registro_parqueo = models.ForeignKey(
        RegistroParqueo, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    # validar si toca add tarifa y estado de la factura ("pagado...")

    def __str__(self):
        return f"Factura {self.id} - cliente: {self.cliente.nombre} - Monto: {self.monto}"
