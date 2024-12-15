from rest_framework import serializers
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo, Tarifa


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
        fields = ['id', 'placa', 'tipo', 'cliente']


class RegistroParqueoSerializer(serializers.ModelSerializer):
    # Relación anidada para mostrar detalles del vehículo
    vehiculo = VehiculoSerializer()
    tiempo_estacionado = serializers.SerializerMethodField()

    class Meta:
        model = RegistroParqueo
        fields = ['id', 'vehiculo', 'fecha_entrada', 'fecha_salida',
                  'tiempo_estacionado', 'total_cobro', 'estado']

    def create(self, validated_data):
        # Extraer los datos del vehiculo del diccionario
        vehiculo_data = validated_data.pop('vehiculo')
        vehiculo_instance, _ = Vehiculo.objects.get_or_create(
            **vehiculo_data)  # Buscar si existe el vehiculo o crearlo

        # crear el registro con la instancia de vehiculo que ya existe
        registro = RegistroParqueo.objects.create(
            vehiculo=vehiculo_instance, **validated_data)
        return registro

    def update(self, instance, validated_data):
        # Extraer los datos del vehiculo del diccionario
        vehiculo_data = validated_data.pop('vehiculo', None)
        if vehiculo_data:
            vehiculo_instance, _ = Vehiculo.objects.get_or_create(
                **vehiculo_data)  # Buscar si existe el vehiculo o crearlo
            instance.vehiculo = vehiculo_instance

        instance = super().update(instance, validated_data)
        return instance

    def get_tiempo_estacionado(self, obj):
        if obj.fecha_entrada and obj.fecha_salida:
            tiempo = (obj.fecha_salida -
                      obj.fecha_entrada).total_seconds() / 60  # En minutos
            return round(tiempo, 2)
        return None


class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = "__all__"
