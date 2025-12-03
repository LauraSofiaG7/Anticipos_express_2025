from django.shortcuts import render, redirect
from django.contrib import messages
from app_administrador.models import Usuario
from django.contrib.auth.hashers import make_password

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
            return redirect("ventas_del_dia")

        elif rol == "Prestamos":
            return redirect("admi_prestamos_gestion")

    return render(request, "login/contraseña.html")
    
def olvide_contraseña_view(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        rol = request.POST.get("rol")

        usuario = Usuario.objects.filter(correo=correo, rol=rol).first()

        if usuario is None:
            messages.error(request, "No existe un usuario con ese correo y rol.")
            return render(request, "login/olvide_contraseña.html")

        return redirect("restablecer_contraseña", usuario_id=usuario.id)

    return render(request, "login/olvide_contraseña.html")



def restablecer_contraseña_view(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == "POST":
        nueva = request.POST.get("nueva")
        confirmar = request.POST.get("confirmar")

        if nueva != confirmar:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "login/restablecer_contraseña.html")

        usuario.contraseña = make_password(nueva)
        usuario.save()

        messages.success(request, "Contraseña actualizada exitosamente.")
        return redirect("inicio_login")

    return render(request, "login/restablecer_contraseña.html")