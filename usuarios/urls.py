from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet

# Crear el router y registrar el ViewSet
router = DefaultRouter()
router.register(r'', UsuarioViewSet, basename='usuario')

# Incluir las rutas generadas por el router
urlpatterns = [
    path('', include(router.urls)),
]
