from django.db import models

# clientes


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    doc_identidad = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.doc_identidad}"
