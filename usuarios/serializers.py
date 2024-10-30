from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.hashers import make_password

# Convierte los datos del modelo a formato JSON y viceversa


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email',
                  'role', 'last_login_date', 'password']
        extra_kwargs = {
            # Se muestra solo en escritura y no en respuesta.
            'password': {'write_only': True}
        }

        def create(self, validated_data):
            # cifrar contraseña antes de guardar
            validated_data['password'] = make_password(
                validated_data['password'])

            return super(UsuarioSerializer, self).create(validated_data)
