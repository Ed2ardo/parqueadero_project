from rest_framework import serializers
from .models import Vehiculo, EspacioParqueo, RegistroParqueo


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


class EspacioParqueoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EspacioParqueo
        fields = '__all__'


class RegistroParqueoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroParqueo
        fields = '__all__'
