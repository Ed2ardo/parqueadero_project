from rest_framework import viewsets, permissions
from .models import Usuario
from .serializers import UsuarioSerializer
from django.contrib.auth.hashers import make_password


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Cifra la contraseña al crear un usuario
        if 'password' in serializer.validated_data:
            serializer.save(password=make_password(
                serializer.validated_data['password']))
        else:
            serializer.save()

    def perform_update(self, serializer):
        # Cifra la contraseña si se está actualizando
        if 'password' in serializer.validated_data:
            serializer.save(password=make_password(
                serializer.validated_data['password']))
        else:
            serializer.save()
