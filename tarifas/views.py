from rest_framework import permissions, viewsets
from .models import Tarifa
from .serializers import TarifaSerializer


class TarifaViewSet(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer
    permission_classes = [permissions.AllowAny]
