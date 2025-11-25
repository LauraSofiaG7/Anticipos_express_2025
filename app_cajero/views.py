from django.shortcuts import render
from app_administrador.models import Usuario


def ventas_del_dia_view(request):
    return render(request, 'cajero/ventas.html')

def registro_view(request):
    return render(request, 'cajero/registro.html')
