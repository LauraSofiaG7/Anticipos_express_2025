from django.shortcuts import render
from app_administrador.models import Usuario

# Create your views here.

def prestamos_inicio(request):
    return render(request, 'prestamos/inicio.html')

def gestion_prestamos(request):
    return render(request, 'prestamos/gestion.html')
