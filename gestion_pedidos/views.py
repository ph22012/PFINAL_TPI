from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from .models import Order, Employee, Customer

def gestion_pedidos(request):
    # Obtener todos los pedidos con sus relaciones necesarias
    pedidos = Order.objects.select_related("employee", "customer").all()

    context = {
        "pedidos": pedidos,
    }
    return render(request, "gestion_pedidos.html", context)

def crear_pedido(request):
    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        productos = request.POST.getlist("productos")  # Lista de productos seleccionados
        cantidades = request.POST.getlist("cantidades")  # Cantidades correspondientes

        # Asignar repartidor automáticamente (ejemplo: el de menos pedidos activos)
        repartidor = Employee.objects.filter(role__name="Repartidor").annotate(
            pedidos_activos=Count("order")
        ).order_by("pedidos_activos").first()

        # Crear el pedido
        pedido = Order.objects.create(
            customer_id=cliente_id,
            employee=repartidor,
            order_status="Pendiente",
        )

        # Redirigir a la vista de gestión de pedidos
        return redirect(gestion_pedidos)

    clientes = Customer.objects.all()
    return render(request, "crear_pedido.html", {"clientes": clientes})

def modificar_pedido(request, pedido_id):
    pedido = get_object_or_404(Order, id=pedido_id)

    if request.method == "POST":
        # Actualizar detalles del pedido según lo recibido en el formulario
        pedido.order_status = request.POST.get("estado", pedido.order_status)
        pedido.employee_id = request.POST.get("repartidor", pedido.employee_id)
        pedido.save()

        return redirect(gestion_pedidos)

    repartidores = Employee.objects.filter(rol__name="Repartidor")
    return render(request, "modificar_pedido.html", {"pedido": pedido, "repartidores": repartidores})

def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Order, id=pedido_id)

    if pedido.order_status != "Entregado":
        pedido.order_status = "Cancelado"
        pedido.save()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "No se puede cancelar un pedido entregado."}, status=400)