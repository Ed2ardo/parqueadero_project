from django.contrib import admin
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo, Tarifa


@admin.register(EspacioParqueoConfig)
class EspacioParqueoConfigAdmin(admin.ModelAdmin):
    list_display = ('tipo_espacio', 'total_espacios', 'espacios_ocupados')
    search_fields = ('tipo_espacio',)
    list_filter = ('tipo_espacio',)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'tipo', 'cliente')
    search_fields = ('placa', 'cliente')
    list_filter = ('tipo',)


@admin.register(RegistroParqueo)
class RegistroParqueoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha_entrada',
                    'fecha_salida', 'total_cobro', 'estado')
    readonly_fields = ('fecha_entrada', 'fecha_salida',
                       'total_cobro', 'estado')
    search_fields = ('vehiculo__placa',)
    list_filter = ('estado', 'fecha_entrada')


@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('tipo_vehiculo', 'costo_por_minuto')
    search_fields = ('tipo_vehiculo',)
    list_filter = ('tipo_vehiculo',)
