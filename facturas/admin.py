from django.contrib import admin
from .models import Factura


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Calcular el total basado en el registro asociado
        if not obj.total:
            tarifa_por_hora = 5000
            tiempo_estacionado = (
                obj.registro.fecha_salida - obj.registro.fecha_entrada).total_seconds() / 3600
            obj.total = tarifa_por_hora * tiempo_estacionado

        # Guardar el objeto después del cálculo
        super().save_model(request, obj, form, change)
    list_display = ('registro', 'identificacion_cliente', 'cliente', 'total')
    # readonly_fields = ('monto', 'tiempo_total', 'fecha_emision', 'tarifa',)
