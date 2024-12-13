from django.db import models
from gestion_parqueadero.models import RegistroParqueo


class Factura(models.Model):
    registro_parqueo = models.OneToOneField(
        RegistroParqueo,
        on_delete=models.CASCADE,
        related_name="factura",
        verbose_name="Registro de Parqueo Asociado"
    )
    fecha_emision = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Emisión")
    numero_factura = models.CharField(
        max_length=20, unique=True, verbose_name="Número de Factura")
    total_cobro = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total Cobrado")
    detalles = models.TextField(
        null=True, blank=True, verbose_name="Detalles Adicionales")

    def __str__(self):
        return f"Factura {self.numero_factura} - Total: {self.total_cobro}"

    def save(self, *args, **kwargs):
        # Generar un número de factura único si no existe
        if not self.numero_factura:
            self.numero_factura = f"FACT-{
                self.id or 'XXXX'}-{self.registro_parqueo.id}"
        super().save(*args, **kwargs)
