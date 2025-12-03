from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio_login'),
    path('contraseña/', views.contraseña_view, name='contraseña'),
    path('login/', views.login_view, name='login'),
    path('olvide-contraseña/', views.olvide_contraseña_view, name='olvide_contraseña'),
    path('restablecer/<int:usuario_id>/', views.restablecer_contraseña_view, name='restablecer_contraseña'),
]
