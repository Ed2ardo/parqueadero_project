from rest_framework import serializers
from .models import Factura


class FacturaSerializer(serializers.ModelSerializer):
    registro_parqueo = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = ['id', 'registro_parqueo', 'fecha_emision',
                  'numero_factura', 'total_cobro', 'detalles']

    def get_registro_parqueo(self, obj):
        return {
            "vehiculo": obj.registro_parqueo.vehiculo.placa,
            "fecha_entrada": obj.registro_parqueo.fecha_entrada,
            "fecha_salida": obj.registro_parqueo.fecha_salida,
            "tiempo_estacionado": obj.registro_parqueo.tiempo_estacionado,
        }
