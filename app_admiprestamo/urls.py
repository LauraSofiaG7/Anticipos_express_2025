from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.prestamos_inicio, name='prestamos_inicio'),
    path('', views.gestion_view, name='prestamos_gestion'),
]
