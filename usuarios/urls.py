from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, LoginView

# Crear el router y registrar el ViewSet
router = DefaultRouter()
router.register(r'', UsuarioViewSet, basename='usuario')

# Incluir las rutas generadas por el router
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
