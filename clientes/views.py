from rest_framework import viewsets, permissions
from .serializers import ClienteSerializer
from .models import Cliente

# clientes

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

