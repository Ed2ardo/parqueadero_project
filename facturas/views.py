from rest_framework import viewsets, status
from rest_framework.response import Response
from gestion_parqueadero.models import RegistroParqueo
from .models import Factura
from .serializers import FacturaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .utils import generar_factura_pdf


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

    def create(self, request, *args, **kwargs):
        registro_id = request.data.get('registro_parqueo_id')
        try:
            registro = RegistroParqueo.objects.get(id=registro_id)
            if not registro.fecha_salida:
                return Response({"error": "El vehículo aún no ha registrado salida."}, status=status.HTTP_400_BAD_REQUEST)

            if Factura.objects.filter(registro_parqueo=registro).exists():
                return Response({"error": "La factura ya ha sido generada para este registro."}, status=status.HTTP_400_BAD_REQUEST)

            # Crear la factura
            factura = Factura.objects.create(
                registro_parqueo=registro,
                total_cobro=registro.total_cobro,
                detalles=request.data.get('detalles', "")
            )
            serializer = self.get_serializer(factura)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except RegistroParqueo.DoesNotExist:
            return Response({"error": "Registro de parqueo no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def descargar_pdf(self, request, pk=None):
        try:
            factura = self.get_object()
            pdf_buffer = generar_factura_pdf(factura)
            return FileResponse(pdf_buffer, as_attachment=True, filename=f"Factura_{factura.numero_factura}.pdf")
        except Factura.DoesNotExist:
            return Response({"error": "Factura no encontrada."}, status=status.HTTP_404_NOT_FOUND)
