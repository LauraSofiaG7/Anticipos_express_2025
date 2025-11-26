from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.prestamos_inicio, name='prestamos_inicio'),
    path('gestion/', views.gestion_prestamos, name='admi_prestamos_gestion'),
]
