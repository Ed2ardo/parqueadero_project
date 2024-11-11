from rest_framework import viewsets, permissions
from .models import Usuario
from .serializers import UsuarioSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({"message": "Test"}, status=status.HTTP_200_OK)
