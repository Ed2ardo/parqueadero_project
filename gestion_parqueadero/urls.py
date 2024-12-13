from rest_framework.routers import DefaultRouter
from .views import EspacioParqueoConfigViewSet, VehiculoViewSet, RegistroParqueoViewSet, TarifaViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'espacios', EspacioParqueoConfigViewSet, basename='espacios')
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculos')
router.register(r'registros', RegistroParqueoViewSet, basename='registros')
router.register(r'tarifas', TarifaViewSet, basename='tarifas')


# Incluir rutas al router
urlpatterns = [
    path('', include(router.urls)),
]
