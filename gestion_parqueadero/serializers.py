from rest_framework import serializers
from .models import Vehiculo, EspacioParqueo, RegistroParqueo


class EspacioParqueoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspacioParqueo
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):
    # Anidado como solo lectura para poder consultar la relación.
    espacio = EspacioParqueoSerializer(read_only=True)

    class Meta:
        model = Vehiculo
        fields = '__all__'


class RegistroParqueoSerializer(serializers.ModelSerializer):
    # vehiculo = VehiculoSerializer(read_only=True)
    vehiculo = serializers.PrimaryKeyRelatedField(
        queryset=Vehiculo.objects.all())

    class Meta:
        model = RegistroParqueo
        fields = ['vehiculo', 'fecha_entrada', 'fecha_salida', 'total_cobro']
