from datetime import datetime, timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import EspacioParqueoConfig, Vehiculo, RegistroParqueo, Tarifa
from .serializers import (
    EspacioParqueoConfigSerializer,
    VehiculoSerializer,
    RegistroParqueoSerializer,
    TarifaSerializer,
)
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
import logging

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


class EspacioParqueoConfigViewSet(viewsets.ModelViewSet):
    queryset = EspacioParqueoConfig.objects.all()
    serializer_class = EspacioParqueoConfigSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def disponibilidad(self, request):
        """Devuelve la disponibilidad de espacios para cada tipo de vehículo."""
        espacios = EspacioParqueoConfig.objects.all()
        data = {
            espacio.tipo_espacio: {
                "total": espacio.total_espacios,
                "ocupados": espacio.espacios_ocupados,
                "disponibles": espacio.total_espacios - espacio.espacios_ocupados,
            }
            for espacio in espacios
        }
        return Response(data)


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """Filtra los vehículos por tipo."""
        tipo = request.query_params.get('tipo')
        if tipo:
            vehiculos = self.queryset.filter(tipo=tipo)
            serializer = self.get_serializer(vehiculos, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "Se debe proporcionar un tipo de vehículo."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RegistroParqueoViewSet(viewsets.ModelViewSet):
    queryset = RegistroParqueo.objects.all()
    serializer_class = RegistroParqueoSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        """Crea un nuevo registro de parqueo y actualiza los espacios ocupados."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vehiculo = serializer.validated_data["vehiculo"]
            tipo_vehiculo = vehiculo.tipo

            # Verificar disponibilidad de espacios
            try:
                espacio_config = EspacioParqueoConfig.objects.get(
                    tipo_espacio=tipo_vehiculo)
                if espacio_config.espacios_ocupados >= espacio_config.total_espacios:
                    return Response(
                        {"error": f"No hay espacios disponibles para {tipo_vehiculo}."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except EspacioParqueoConfig.DoesNotExist:
                return Response(
                    {"error": f"No se encontró configuración para {tipo_vehiculo}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Crear registro
            registro = serializer.save()

            # Actualizar espacios ocupados
            espacio_config.espacios_ocupados += 1
            espacio_config.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def registrar_salida(self, request, pk=None):
        """Registra la salida de un vehículo, calcula el tiempo estacionado y actualiza los espacios."""
        try:
            registro = self.get_object()

            # Validar si ya se registró la salida
            if registro.fecha_salida is not None:
                return Response(
                    {"error": "La salida ya ha sido registrada."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Registrar fecha y hora de salida
            registro.fecha_salida = datetime.now(timezone.utc)

            # Calcular tiempo estacionado en minutos
            tiempo_estacionado = (
                Decimal((registro.fecha_salida -
                        registro.fecha_entrada).total_seconds()) / Decimal(60)
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            registro.tiempo_estacionado = tiempo_estacionado

            # Obtener la tarifa del tipo de vehículo
            tarifa = Tarifa.objects.filter(
                tipo_vehiculo=registro.vehiculo.tipo).first()
            if not tarifa:
                return Response(
                    {"error": "No se encontró una tarifa para este tipo de vehículo."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Calcular el total a cobrar
            try:
                costo_por_minuto = Decimal(tarifa.costo_por_minuto)
                total_cobro = (tiempo_estacionado * costo_por_minuto).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
                registro.total_cobro = total_cobro
            except InvalidOperation:
                return Response(
                    {"error": "Error al calcular el total a cobrar. Verifique los datos de la tarifa."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Actualizar espacios ocupados
            espacio_config = EspacioParqueoConfig.objects.filter(
                tipo_espacio=registro.vehiculo.tipo).first()
            if espacio_config:
                espacio_config.espacios_ocupados = max(
                    espacio_config.espacios_ocupados - 1, 0)
                espacio_config.save()

            # Guardar registro actualizado
            registro.estado = "facturado"
            registro.save()

            # Registrar en log de auditoría
            auditor_logger.info(
                f"Salida registrada para el vehículo {registro.vehiculo.placa}. Tiempo estacionado: {
                    registro.tiempo_estacionado} minutos. Total cobrado: {registro.total_cobro}."
            )

            # Serializar y devolver el registro actualizado
            serializer = self.get_serializer(registro)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Loguear el error
            auditor_logger.error(
                f"Error al registrar salida para el registro {pk}: {str(e)}")
            return Response(
                {"error": "Ocurrió un error al procesar la solicitud. Intente nuevamente."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
