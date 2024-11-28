from django.contrib import admin
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo


@admin.register(EspacioParqueoConfig)
class EspacioParqueoConfigAdmin(admin.ModelAdmin):
    list_display = ('tipo_espacio', 'total_espacios')


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'tipo', 'hora_entrada')


@admin.register(RegistroParqueo)
class RegistroParqueoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha_entrada', 'fecha_salida', 'total_cobro')
    readonly_fields = ('fecha_entrada', 'total_cobro')
