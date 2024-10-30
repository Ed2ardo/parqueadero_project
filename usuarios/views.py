from rest_framework import generics, permissions
# from rest_framework.permissions import IsAuthenticated
from .models import Usuario
from .serializers import UsuarioSerializer

# views users

# List and create users


class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()  # datos disponibles: todos los objetos de Usuario
    serializer_class = UsuarioSerializer
    # Restringe el acceso a usuarios autenticados.
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save()

# obtener, update y eliminar usuarios especificos


class UsuarioGestionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
