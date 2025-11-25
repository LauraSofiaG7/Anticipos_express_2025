from django.urls import path
from . import views

urlpatterns = [
    path('ventas-dia/', views.ventas_del_dia_view, name='ventas_del_dia'),
    path('registro/', views.registro_view, name='cajero_registro'),
]