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

        # 1. Buscar SOLO por correo
        usuario = Usuario.objects.filter(correo=correo).first()

        if usuario is None:
            messages.error(request, "El correo no existe.")
            return render(request, "login/contraseña.html")

        # 2. Validar rol ANTES de validar contraseña
        if usuario.rol != rol:
            messages.error(request, "El rol seleccionado no coincide con tu cuenta.")
            return render(request, "login/contraseña.html")

        # 3. Validar contraseña SOLO si el rol coincide
        if usuario.contraseña != contraseña:
            messages.error(request, "Contraseña incorrecta.")
            return render(request, "login/contraseña.html")


        # Redirigir según el rol
        if usuario.rol == "Administrador":
            return redirect("admin_inicio")   

        elif usuario.rol == "Vendedor":
            return redirect("vendedor_nueva_venta")

        elif usuario.rol == "Cajero":
            return redirect("cajero_registro") 

        elif usuario.rol == "Prestamos":
            return redirect("prestamos_gestion")  

        else:
            messages.error(request, "Rol desconocido.")
            return render(request, "login/contraseña.html")

    return render(request, "login/contraseña.html")
