from rest_framework import serializers
from .models import Factura
from gestion_parqueadero.models import RegistroParqueo
from tarifas.models import Tarifa


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
        read_only_fields = ['monto', 'tiempo_total', 'fecha_emision']

    def create(self, validated_data):
        registro = validated_data['registro_parqueo']

        # 1. Calcular el tiempo total
        tiempo_total = registro.fecha_salida - registro.fecha_entrada
        validated_data['tiempo_total'] = tiempo_total

        # 2. Obtener la tarifa según el tipo vehículo:
        tipo_vehiculo = registro.vehiculo.tipo
        tarifa = Tarifa.objects.get(tipo_vehiculo=tipo_vehiculo)

        # 3. Calcular el monto:
        horas_estacionadas = tiempo_total.total_seconds() / 3600  # Convierte segundos a horas
        monto = tarifa.costo_por_hora * horas_estacionadas
        validated_data['monto'] = monto
        validated_data['tarifa'] = tarifa

        return super().create(validated_data)
