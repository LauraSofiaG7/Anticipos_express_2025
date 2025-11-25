from django.shortcuts import render
from app_administrador.models import Usuario

# Create your views here.
def prestamos_inicio(request):
    return render(request, 'admiprestamo/gestion.html')
def gestion_view(request):
    return render(request, 'admiprestamo/gestion.html')