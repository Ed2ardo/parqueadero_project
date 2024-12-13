from rest_framework import serializers
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo


class EspacioParqueoConfigSerializer(serializers.ModelSerializer):
    espacios_ocupados = serializers.IntegerField(
        source='espacios_ocupados', read_only=True)
    espacios_disponibles = serializers.SerializerMethodField()

    class Meta:
        model = EspacioParqueoConfig
        fields = ['id', 'tipo_espacio', 'total_espacios',
                  'espacios_ocupados', 'espacios_disponibles']

    def get_espacios_disponibles(self, obj):
        return obj.total_espacios - obj.espacios_ocupados


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['id', 'placa', 'tipo']


class RegistroParqueoSerializer(serializers.ModelSerializer):
    # Relación anidada para mostrar detalles del vehículo
    vehiculo = VehiculoSerializer()
    tiempo_estacionado = serializers.SerializerMethodField()

    class Meta:
        model = RegistroParqueo
        fields = ['id', 'vehiculo', 'fecha_entrada', 'fecha_salida',
                  'tiempo_estacionado', 'total_cobro', 'estado']

    def get_tiempo_estacionado(self, obj):
        if obj.fecha_entrada and obj.fecha_salida:
            tiempo = (obj.fecha_salida -
                      obj.fecha_entrada).total_seconds() / 60  # En minutos
            return round(tiempo, 2)
        return None
