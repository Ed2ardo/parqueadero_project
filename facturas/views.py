from rest_framework import viewsets, permissions
from .models import Factura
from .serializers import FacturaSerializer

# views - facturas


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [permissions.IsAuthenticated]
