from django.shortcuts import render
from app_administrador.models import Usuario


def nueva_venta_view(request):
    return render(request, 'vendedor/nueva_venta.html')


def consulta_productos_view(request):
    return render(request, 'vendedor/consulta_productos.html')

def revision_deudas_view(request):
    return render(request, 'vendedor/revision_deudas.html')
