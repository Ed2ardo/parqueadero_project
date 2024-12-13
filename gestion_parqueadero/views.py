from datetime import datetime, timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo, Tarifa
from .serializers import EspacioParqueoConfigSerializer, VehiculoSerializer, RegistroParqueoSerializer
from rest_framework.permissions import AllowAny
import logging

# Configurar el logger para auditoría
auditor_logger = logging.getLogger("auditor")
auditor_logger.setLevel(logging.INFO)
handler = logging.FileHandler("auditoria_parqueadero.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
auditor_logger.addHandler(handler)


# ViewSet para la configuración de espacios
class EspacioParqueoConfigViewSet(viewsets.ModelViewSet):
    queryset = EspacioParqueoConfig.objects.all()
    serializer_class = EspacioParqueoConfigSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def disponibilidad(self, request):
        espacios = EspacioParqueoConfig.objects.all()
        data = {
            espacio.tipo_espacio: {
                "total": espacio.total_espacios,
                "ocupados": espacio.espacios_ocupados,
                "disponibles": espacio.total_espacios - espacio.espacios_ocupados,
            } for espacio in espacios
        }
        return Response(data)


# ViewSet para los vehículos
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'])
    def registrar_salida(self, request, pk=None):
        try:
            registro = self.get_object()
            if registro.fecha_salida is not None:
                return Response({"error": "La salida ya ha sido registrada."}, status=status.HTTP_400_BAD_REQUEST)

            # Calcular fecha de salida automáticamente
            registro.fecha_salida = datetime.now(timezone.utc)

            # Calcular tiempo estacionado en minutos
            tiempo_estacionado = (registro.fecha_salida -
                                  registro.fecha_entrada).total_seconds() / 60
            registro.tiempo_estacionado = round(tiempo_estacionado, 2)

            # Obtener tarifa del tipo de vehículo
            tarifa = Tarifa.objects.filter(
                tipo_vehiculo=registro.vehiculo.tipo).first()
            if not tarifa:
                return Response({"error": "No se encontró una tarifa para este tipo de vehículo."}, status=status.HTTP_400_BAD_REQUEST)

            # Calcular total a cobrar
            registro.total_cobro = round(
                tiempo_estacionado * tarifa.costo_por_minuto, 2)

            # Actualizar espacios ocupados
            espacio_config = EspacioParqueoConfig.objects.filter(
                tipo_espacio=registro.vehiculo.tipo).first()
            if espacio_config:
                espacio_config.espacios_ocupados = max(
                    espacio_config.espacios_ocupados - 1, 0)
                espacio_config.save()

            registro.save()

            # Registrar auditoría
            auditor_logger.info(f"Salida registrada para el vehículo {registro.vehiculo.placa}. Tiempo: {
                                registro.tiempo_estacionado} minutos. Total cobrado: {registro.total_cobro}.")

            return Response({
                "mensaje": "Salida registrada exitosamente.",
                "tiempo_estacionado": registro.tiempo_estacionado,
                "total_cobro": registro.total_cobro
            })
        except Exception as e:
            auditor_logger.error(
                f"Error al registrar salida para el registro {pk}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def dar_baja(self, request, pk=None):
        try:
            registro = self.get_object()
            if registro.estado != 'activo':
                return Response({"error": "El vehículo no está activo."}, status=status.HTTP_400_BAD_REQUEST)

            registro.estado = 'baja'
            registro.save()

            # Liberar espacio ocupado
            espacio_config = EspacioParqueoConfig.objects.filter(
                tipo_espacio=registro.vehiculo.tipo).first()
            if espacio_config:
                espacio_config.espacios_ocupados = max(
                    espacio_config.espacios_ocupados - 1, 0)
                espacio_config.save()

            # Registrar auditoría
            auditor_logger.info(f"Registro dado de baja para el vehículo {
                                registro.vehiculo.placa}. Estado actualizado a 'baja'.")

            return Response({"mensaje": "Registro dado de baja exitosamente."}, status=status.HTTP_200_OK)
        except RegistroParqueo.DoesNotExist:
            auditor_logger.error(f"Error al dar de baja el registro {
                                 pk}: No encontrado.")
            return Response({"error": "Registro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
