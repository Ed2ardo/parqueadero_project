from rest_framework.routers import DefaultRouter
from .views import FacturaViewSet

router = DefaultRouter()
router.register(r'', FacturaViewSet, basename='facturas')

urlpatterns = router.urls
# descargar el pdf: GET /api/facturas/<id>/descargar_pdf/
