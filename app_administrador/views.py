from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date, timedelta

from app_administrador.models import Cliente, Producto, Categoria, Venta, CuentaPorCobrar


# ==============================
# DASHBOARD
# ==============================
def admin_inicio(request):
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)

    ingresos_mes = Venta.objects.filter(fecha__gte=inicio_mes).aggregate(total=Sum("total"))["total"] or 0

    inicio_mes_pasado = (inicio_mes - timedelta(days=1)).replace(day=1)
    fin_mes_pasado = inicio_mes - timedelta(days=1)
    ingresos_mes_pasado = Venta.objects.filter(
        fecha__range=(inicio_mes_pasado, fin_mes_pasado)
    ).aggregate(total=Sum("total"))["total"] or 0

    crecimiento = ((ingresos_mes - ingresos_mes_pasado) / ingresos_mes_pasado * 100) if ingresos_mes_pasado > 0 else 100

    clientes_deuda = Cliente.objects.filter(deuda_total__gt=0).count()
    texto_clientes_deuda = f"{clientes_deuda} clientes con deuda"

    total_productos = Producto.objects.count()
    categorias_activas = Categoria.objects.count()

    # Productos con stock bajo (≤2)
    productos_stock_bajo = Producto.objects.filter(stock__lte=2)
    alertas_stock = productos_stock_bajo.count()

# Pagos fiados próximos 5 días
    proximos_5 = hoy + timedelta(days=5)
    pagos_fiados = CuentaPorCobrar.objects.filter(
    estado="Pendiente",
    fecha_vencimiento__lte=proximos_5   ).order_by("fecha_vencimiento")[:5]

    contexto = {
        "ingresos_mes": ingresos_mes,
        "crecimiento": round(crecimiento, 2),
        "clientes_deuda": clientes_deuda,
        "clientes_con_deuda": texto_clientes_deuda,
        "total_productos": total_productos,
        "categorias_activas": categorias_activas,
        "alertas_stock": alertas_stock,
        "productos_stock_bajo": productos_stock_bajo,
        "pagos_fiados": pagos_fiados,
    }

    return render(request, "administrador/inicio.html", contexto)


# ==============================
# CLIENTES
# ==============================
def admin_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'administrador/clientes.html', {"clientes": clientes})


def agregar_cliente(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        deuda = request.POST.get("deuda", 0)
        documento = request.POST.get("documento_identidad")
        correo = request.POST.get("correo") or None  # correo opcional

        Cliente.objects.create(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            deuda_total=deuda,
            documento_identidad=documento
        )

        return redirect('admin_clientes')

    return redirect('admin_clientes')


def editar_cliente(request):
    if request.method == "POST":
        cliente_id = request.POST.get("id")
        cliente = get_object_or_404(Cliente, id=cliente_id)

        cliente.nombre = request.POST.get("nombre")
        cliente.telefono = request.POST.get("telefono")
        cliente.documento_identidad = request.POST.get("documento_identidad")
        cliente.correo = request.POST.get("correo") or None
        cliente.deuda_total = request.POST.get("deuda")

        cliente.save()

    return redirect("admin_clientes")


def marcar_saldada(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.deuda_total = 0
    cliente.save()

    return JsonResponse({"ok": True})
