from django.shortcuts import render
from app_administrador.models import Usuario

# Create your views here.
def admin_inicio(request):
    return render(request, 'administrador/inicio.html')
def admin_clientes(request):
    return render(request, 'administrador/clientes.html')

def admin_productos(request):
    return render(request, 'administrador/productos.html')

def admin_cuentas(request):
    return render(request, 'administrador/cuentas.html')

def admin_reportes(request):
    return render(request, 'administrador/reportes.html')