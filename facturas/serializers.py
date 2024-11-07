from rest_framework import serializers
from .models import Factura
from gestion_parqueadero.models import RegistroParqueo
from tarifas.models import Tarifa


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
        read_only_fields = ['monto', 'tiempo_total', 'fecha_emision']
