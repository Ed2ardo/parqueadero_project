from rest_framework import viewsets, permissions
from .models import Vehiculo, EspacioParqueo, RegistroParqueo
from .serializers import VehiculoSerializer, EspacioParqueoSerializer, RegistroParqueoSerializer

# views: GestionParqueadero


# ---- Vehiculo views ----
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAuthenticated]


#  --- EspacioPArqueo Views ---
class EspacioParqueoViewSet(viewsets.ModelViewSet):
    queryset = EspacioParqueo.objects.all()
    serializer_class = EspacioParqueoSerializer
    permission_classes = [permissions.IsAuthenticated]


#  --- RegistroParqueo Views ---
class RegistroParqueoViewSet(viewsets.ModelViewSet):
    queryset = RegistroParqueo.objects.all()
    serializer_class = RegistroParqueoSerializer
    permission_classes = [permissions.IsAuthenticated]
