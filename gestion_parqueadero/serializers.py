from rest_framework import serializers
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo


class EspacioParqueoConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspacioParqueoConfig
        fields = ['id', 'tipo_espacio', 'total_espacios']


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['id', 'placa', 'tipo', 'hora_entrada', 'cliente']


class RegistroParqueoSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(read_only=True)

    class Meta:
        model = RegistroParqueo
        fields = ['id', 'vehiculo', 'fecha_entrada',
                  'fecha_salida', 'total_cobro']
