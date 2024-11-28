from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    doc_identidad = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True,
                              validators=[EmailValidator()])
    telefono = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex='^/d{10}$', message='El teléfono debe contener exactamente 10 dígitos.')]
    )
    direccion = models.TextField(max_length=100, blank=True, null=True)

    def clean(self):
        if not self.nombre:
            raise ValidationError("El nombre no puede estar vacío.")

    def __str__(self):
        return f"{self.nombre} - {self.doc_identidad}"
