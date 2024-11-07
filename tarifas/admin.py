from django.contrib import admin
from .models import Tarifa


@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('tipo_vehiculo', 'costo_por_hora')
