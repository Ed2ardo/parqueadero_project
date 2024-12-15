from datetime import datetime, timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo, Tarifa
from .serializers import EspacioParqueoConfigSerializer, VehiculoSerializer, RegistroParqueoSerializer, TarifaSerializer
from rest_framework.permissions import AllowAny
import logging
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

# Configurar el logger para auditoría
auditor_logger = logging.getLogger("auditor")
auditor_logger.setLevel(logging.INFO)
handler = logging.FileHandler("auditoria_parqueadero.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
auditor_logger.addHandler(handler)


class TarifaViewSet(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer
    permission_classes = [AllowAny]


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

            # Validar si ya se registró la salida
            if registro.fecha_salida is not None:
                return Response(
                    {"error": "La salida ya ha sido registrada."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Registrar fecha de salida
            registro.fecha_salida = datetime.now(timezone.utc)

            # Calcular tiempo estacionado en minutos (convertido a Decimal)
            tiempo_estacionado = (
                Decimal((registro.fecha_salida -
                        registro.fecha_entrada).total_seconds())
                / Decimal(60)
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            registro.tiempo_estacionado = tiempo_estacionado

            # Obtener tarifa del tipo de vehículo
            tarifa = Tarifa.objects.filter(
                tipo_vehiculo=registro.vehiculo.tipo).first()
            if not tarifa:
                return Response(
                    {"error": "No se encontró una tarifa para este tipo de vehículo."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Calcular total a cobrar
            try:
                costo_por_minuto = Decimal(tarifa.costo_por_minuto)
                total_cobro = (tiempo_estacionado * costo_por_minuto).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
                registro.total_cobro = total_cobro
            except InvalidOperation as e:
                return Response(
                    {"error": "Error al calcular el total a cobrar. Verifique los datos de la tarifa."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Actualizar espacios ocupados
            espacio_config = EspacioParqueoConfig.objects.filter(
                tipo_espacio=registro.vehiculo.tipo
            ).first()
            if espacio_config:
                espacio_config.espacios_ocupados = max(
                    espacio_config.espacios_ocupados - 1, 0
                )
                espacio_config.save()

            # Guardar cambios en el registro
            registro.estado = "facturado"
            registro.save()

            # Registrar auditoría
            auditor_logger.info(
                f"Salida registrada para el vehículo {
                    registro.vehiculo.placa}. "
                f"Tiempo: {registro.tiempo_estacionado} minutos. Total cobrado: {
                    registro.total_cobro}."
            )

            # Serializar y devolver el registro actualizado
            serializer = self.get_serializer(registro)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            auditor_logger.error(
                f"Error al registrar salida para el registro {pk}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
