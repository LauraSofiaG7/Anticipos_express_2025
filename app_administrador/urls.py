from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.admin_inicio, name="admin_inicio"),
    path('clientes/', views.admin_clientes, name="admin_clientes"),
    path('productos/', views.admin_productos, name="admin_productos"),
    path('cuentas/', views.admin_cuentas, name="admin_cuentas"),
    path('reportes/', views.admin_reportes, name="admin_reportes"),
    path('admin/clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/editar/', views.editar_cliente, name='editar_cliente'),
    
    # RUTA CORREGIDA: Cambiada para que coincida con la llamada del JavaScript
    path("marcar_saldada/<int:cliente_id>/", views.marcar_saldada, name="marcar_saldada"),
]