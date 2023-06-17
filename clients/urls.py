from django.urls import path, include
from rest_framework.documentation import include_docs_urls # Importación para documentar co coreapi
from rest_framework import routers
from clients import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Las rutas de la API se agregarán a la raíz de la URL.
    path('docs/', include_docs_urls(title='Clients API')) # Ruta de la documentación
]