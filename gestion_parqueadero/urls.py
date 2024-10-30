from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VehiculoViewSet, EspacioParqueoViewSet, RegistroParqueoViewSet


# Crear router y registrar los ViewSets
router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'espacios', EspacioParqueoViewSet, basename='espacioparqueo')
router.register(r'registros', RegistroParqueoViewSet,
                basename='registroparqueo')

# Incluir rutas al router
urlpatterns = [
    path('', include(router.urls))
]
