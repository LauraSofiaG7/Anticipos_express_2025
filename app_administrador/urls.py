from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.admin_inicio, name='admin_inicio'),
    path('clientes/', views.admin_clientes, name='admin_clientes'),
    path('productos/', views.admin_productos, name='admin_productos'),
    path('cuentas/', views.admin_cuentas, name='admin_cuentas'),
    path('reportes/', views.admin_reportes, name='admin_reportes'),
]
