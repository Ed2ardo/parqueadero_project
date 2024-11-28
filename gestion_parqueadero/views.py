from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo
from .serializers import EspacioParqueoConfigSerializer, VehiculoSerializer, RegistroParqueoSerializer


# ViewSet para la configuración de espacios
class EspacioParqueoConfigViewSet(viewsets.ModelViewSet):
    queryset = EspacioParqueoConfig.objects.all()
    serializer_class = EspacioParqueoConfigSerializer


# ViewSet para los vehículos
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    # Filtrar vehículos por tipo
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        tipo = request.query_params.get('tipo', None)
        if tipo:
            vehiculos = self.queryset.filter(tipo=tipo)
            serializer = self.get_serializer(vehiculos, many=True)
            return Response(serializer.data)
        return Response({"error": "Se debe proporcionar un tipo de vehículo."}, status=status.HTTP_400_BAD_REQUEST)


# ViewSet para los registros de parqueo
class RegistroParqueoViewSet(viewsets.ModelViewSet):
    queryset = RegistroParqueo.objects.all()
    serializer_class = RegistroParqueoSerializer

    # Endpoint personalizado para registrar salida de un vehículo
    @action(detail=True, methods=['post'])
    def registrar_salida(self, request, pk=None):
        try:
            registro = self.get_object()
            if registro.fecha_salida is not None:
                return Response({"error": "La salida ya ha sido registrada."}, status=status.HTTP_400_BAD_REQUEST)

            registro.fecha_salida = request.data.get('fecha_salida')
            registro.total_cobro = request.data.get('total_cobro')
            registro.save()
            return Response({"mensaje": "Salida registrada exitosamente."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
