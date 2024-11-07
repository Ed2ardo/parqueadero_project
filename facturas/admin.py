from django.contrib import admin
from .models import Factura


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'registro_parqueo', 'tarifa',
                    'monto', 'tiempo_total', 'fecha_emision')

    readonly_fields = ('monto', 'tiempo_total', 'fecha_emision', 'tarifa',)
