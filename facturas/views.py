from rest_framework import viewsets, permissions
from .models import Factura, Tarifa
from .serializers import FacturaSerializer
from rest_framework.exceptions import ValidationError


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Obtener el registro del parqueo asociado a la factura
        registro = serializer.validated_data['registro_parqueo']
        tipo_vehiculo = registro.vehiculo.tipo

        # Verificar si existe una tarifa para el tipo de vehículo
        tarifa = Tarifa.objects.filter(tipo_vehiculo=tipo_vehiculo).first()
        if not tarifa:
            raise ValidationError(
                f"No existe una tarifa configurada para el tipo de vehículo: {tipo_vehiculo}.")

        # Crear la factura si todo es válido
        serializer.save()
