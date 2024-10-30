from django.urls import path
# from rest_framework.routers import DefaultRouter
from .views import UsuarioGestionView, UsuarioListCreateView

# router = DefaultRouter()  # Genera las rutas para la vista de UsuarioViewSet
# # registrar la ruta en "usuarios/"
# router.register(r'usuarios', UsuarioViewSet)


# Definir las rutas de la API, incluida las de router
urlpatterns = [
    path('', UsuarioListCreateView.as_view(),
         name='user-list-create'),  # GET & POST
    path('<int:pk>/', UsuarioGestionView.as_view(),
         name='user-detail'),  # GET, PUT & DELETE
]
