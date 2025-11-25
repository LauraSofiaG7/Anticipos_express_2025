from django.urls import path
from . import views

urlpatterns = [
    path('nueva-venta/', views.nueva_venta_view, name='vendedor_nueva_venta'),
    path('consulta-productos/', views.consulta_productos_view, name='vendedor_consulta_productos'),
    path('revision-deudas/', views.revision_deudas_view, name='vendedor_revision_deudas'),
]
