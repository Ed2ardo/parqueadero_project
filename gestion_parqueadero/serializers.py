from rest_framework import serializers
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo, Tarifa


class EspacioParqueoConfigSerializer(serializers.ModelSerializer):
    # Calcula espacios ocupados y disponibles automáticamente
    espacios_ocupados = serializers.IntegerField(read_only=True)
    espacios_disponibles = serializers.SerializerMethodField()

    class Meta:
        model = EspacioParqueoConfig
        fields = ['id', 'tipo_espacio', 'total_espacios',
                  'espacios_ocupados', 'espacios_disponibles']

    def get_espacios_disponibles(self, obj):
        # Calcula espacios disponibles en tiempo real
        return obj.total_espacios - obj.espacios_ocupados


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['id', 'placa', 'tipo', 'cliente']


class RegistroParqueoSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer()  # Relación anidada para incluir datos del vehículo
    tiempo_estacionado = serializers.SerializerMethodField()

    class Meta:
        model = RegistroParqueo
        fields = ['id', 'vehiculo', 'fecha_entrada', 'fecha_salida',
                  'tiempo_estacionado', 'total_cobro', 'estado']

    def create(self, validated_data):
        # Extraer y gestionar los datos del vehículo
        vehiculo_data = validated_data.pop('vehiculo')
        vehiculo_instance, _ = Vehiculo.objects.get_or_create(**vehiculo_data)
        validated_data['vehiculo'] = vehiculo_instance
        return RegistroParqueo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Actualizar los datos del vehículo si están presentes
        vehiculo_data = validated_data.pop('vehiculo', None)
        if vehiculo_data:
            vehiculo_instance, _ = Vehiculo.objects.get_or_create(
                **vehiculo_data)
            instance.vehiculo = vehiculo_instance
        return super().update(instance, validated_data)

    def get_tiempo_estacionado(self, obj):
        # Calcula el tiempo estacionado solo si hay entrada y salida
        if obj.fecha_entrada and obj.fecha_salida:
            tiempo = (obj.fecha_salida -
                      obj.fecha_entrada).total_seconds() / 60
            return round(tiempo, 2)
        return None


class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = "__all__"
