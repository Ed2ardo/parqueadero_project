from django.contrib import admin
from .models import EspacioParqueo, Vehiculo, RegistroParqueo


@admin.register(EspacioParqueo)
class EspacioParqeoAdmin(admin.ModelAdmin):
    list_display = ('numero_espacio', 'estado', 'tipo_espacio')


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'tipo', 'espacio')


@admin.register(RegistroParqueo)
class RegistroParqueoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha_entrada', 'fecha_salida', 'total_cobro')
    readonly_fields = ('fecha_entrada',)
