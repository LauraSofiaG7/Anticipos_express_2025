from django.shortcuts import render, redirect
from django.contrib import messages
from app_administrador.models import Usuario

def inicio_view(request):
    return render(request, 'login/inicio.html')

def contraseña_view(request):
    return render(request, 'login/contraseña.html')


def login_view(request):
    if request.method == "POST":

        correo = request.POST.get("email")
        contraseña = request.POST.get("password")
        rol = request.POST.get("rol")

        # Buscar usuario por correo
        usuario = Usuario.objects.filter(correo=correo).first()

        if usuario is None:
            messages.error(request, "El correo no existe.")
            return render(request, "login/contraseña.html")

        # VALIDACIÓN DE CONTRASEÑAS POR ROL
        contraseñas_roles = {
            "Administrador": "admi2025",
            "Vendedor": "vendedor2025",
            "Cajero": "cajero2025",
            "Prestamos": "prestamos2025",
        }

        # Si el rol no existe en la tabla de contraseñas
        if rol not in contraseñas_roles:
            messages.error(request, "Rol inválido.")
            return render(request, "login/contraseña.html")

        # Comparar contraseña según el rol elegido
        if contraseña != contraseñas_roles[rol]:
            messages.error(request, "Contraseña incorrecta para el rol seleccionado.")
            return render(request, "login/contraseña.html")

        # REDIRECCIÓN SEGÚN ROL
        if rol == "Administrador":
            return redirect("admin_inicio")

        elif rol == "Vendedor":
            return redirect("vendedor_nueva_venta")

        elif rol == "Cajero":
            return redirect("cajero_registro")

        elif rol == "Prestamos":
            return redirect("admi_prestamos_gestion")

    return render(request, "login/contraseña.html")
