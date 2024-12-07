from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from gestion_pedidos.models import Employee
from moduloDespacho.models import Order_status, Order
from django.utils.timezone import now
from django.db.models import Sum

def repartidores_index(request):
    repartidor = get_object_or_404(Employee, id=request.user.id, id_rol__name="Repartidor")

    # Obtener pedidos asignados al repartidor
    pedidos = Order.objects.filter(employee=repartidor).exclude(status__status="Entregado").order_by('order_date')

    # Calcular el total de cada pedido
    pedidos_con_totales = []
    for pedido in pedidos:
        total = pedido.shoppingcart.detail_set.aggregate(total=Sum('sub_total'))['total'] or 0
        pedidos_con_totales.append({
            'pedido': pedido,
            'total': total
        })

    return render(request, 'index.html', {
        'repartidor': repartidor,
        'pedidos_con_totales': pedidos_con_totales,
    })

def activar_repartidor(request):
    repartidor = get_object_or_404(Employee, id=request.user.id, id_rol__name="Repartidor")
    repartidor.is_active = True
    repartidor.save()
    messages.success(request, "Te has activado exitosamente.")
    return redirect('repartidores:index')

def desactivar_repartidor(request):
    repartidor = get_object_or_404(Employee, id=request.user.id, id_rol__name="Repartidor")
    repartidor.is_active = False
    repartidor.save()
    messages.success(request, "Te has desactivado exitosamente.")
    return redirect('repartidores:index')

def entregar_pedido(request, pedido_id):
    pedido = get_object_or_404(Order, id=pedido_id, employee=request.user.id)
    pedido.status = Order_status.objects.get(status="Entregado")
    pedido.last_update = now()
    pedido.save()
    messages.success(request, f"El pedido #{pedido.id} se ha marcado como entregado.")
    return redirect('repartidores:index')