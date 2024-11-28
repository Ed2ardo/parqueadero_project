from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError


class Usuario(AbstractUser):
    role = models.CharField(max_length=50, choices=[(
        'admin', 'Administrador'), ('operario', 'Operario')])
    last_login_date = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        # Cambia el related_name para evitar el conflicto
        related_name='usuarios_usuario_groups',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="usuarios_usuario_permissions",
        blank=True
    )

    def clean(self):
        if self.role not in ['admin', 'operario']:
            raise ValidationError("El rol debe ser 'admin' o 'operario'.")

    def __str__(self):
        return self.username
