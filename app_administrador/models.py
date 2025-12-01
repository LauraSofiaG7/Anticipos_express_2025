from django.db import models


# ===========================
#   USUARIO
# ===========================
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=255)

    ROLES = [
        ("Administrador", "Administrador"),
        ("Vendedor", "Vendedor"),
        ("Cajero", "Cajero"),
        ("Prestamos", "Prestamos"),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default="Administrador")

    def __str__(self):
        return f"{self.nombre} ({self.rol})"


# ===========================
#   CLIENTE
# ===========================
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    documento_identidad = models.CharField(max_length=50)
    correo = models.EmailField(null=True, blank=True)
    # Importante: Usar DecimalField para dinero real para evitar problemas de precisión,
    # pero mantendremos IntegerField como lo tenías.
    deuda_total = models.DecimalField(max_digits=12, decimal_places=2, default=0) 
    estado = models.CharField(max_length=50, default="Activo") 

    def __str__(self):
        return f"{self.nombre} - {self.documento_identidad}"


# ===========================
#   CATEGORÍA
# ===========================
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# ===========================
#   PRODUCTO
# ===========================
class Producto(models.Model):
    class Condicion(models.TextChoices):
        NUEVO = "Nuevo", "Nuevo"
        USADO = "Usado", "Usado"

    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    condicion = models.CharField(
        max_length=10,
        choices=Condicion.choices,
        default=Condicion.NUEVO
    )
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField()
    estado = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)

    # Categoría verdadera
    categoria = models.ForeignKey(
        "Categoria",
        on_delete=models.CASCADE,
        related_name="productos"
    )

    def __str__(self):
        return f"{self.nombre} ({self.marca}) - {self.condicion}"


# ===========================
#   VENTA
# ===========================
class Venta(models.Model):
    class MetodoPago(models.TextChoices):
        CONTADO = "Contado", "Contado"
        CREDITO = "Credito", "Credito"

    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE, related_name="ventas")
    vendedor = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name="ventas_realizadas")
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(
        max_length=10,
        choices=MetodoPago.choices,
        default=MetodoPago.CONTADO
    )

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.cliente.nombre} - Total: ${self.total:.2f}"


# ===========================
#   DETALLE VENTA
# ===========================
class DetalleVenta(models.Model):
    venta = models.ForeignKey("Venta", on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE, related_name="detalles")
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Detalle #{self.id} - {self.producto.nombre} x {self.cantidad}"


# ===========================
#   CUENTAS POR COBRAR
# ===========================
class CuentaPorCobrar(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "Pendiente", "Pendiente"
        PAGADA = "Pagada", "Pagada"

    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE, related_name="cuentas_por_cobrar")
    venta = models.ForeignKey("Venta", on_delete=models.CASCADE, related_name="cuentas_por_cobrar")
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_prestamo = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE)

    def __str__(self):
        return f"Cuenta #{self.id} - {self.cliente.nombre} - {self.estado}"


# ===========================
#   CAJA (Módulo Cajero)
# ===========================
class Caja(models.Model):
    cajero = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name="cajas")
    fondo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    ventas_efectivo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_caja = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Caja #{self.id} - Cajero: {self.cajero.nombre}"


# ===========================
#   ROL (Opcional)
# ===========================
class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre


# ===========================
#   PRÉSTAMO
# ===========================
class Prestamo(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = "Activo", "Activo"
        PAGADO = "Pagado", "Pagado"
        VENCIDO = "Vencido", "Vencido"

    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE, related_name="prestamos")
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)
    fecha_prestamo = models.DateField()
    fecha_proximo_pago = models.DateField()
    cuotas_restantes = models.IntegerField()

    def __str__(self):
        return f"Préstamo #{self.id} - {self.cliente.nombre} - {self.estado}"


# ===========================
#   CONDICIÓN PRODUCTO
# ===========================
class CondicionProducto(models.Model):
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE, related_name="condiciones")
    descripcion = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return f"Condición #{self.id} - {self.producto.nombre}"