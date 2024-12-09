from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from modulo_administracion.models import Employee, CustomUser
from moduloDespacho.models import Order_status, Order
from django.utils.timezone import now
from django.db.models import Sum

def repartidores_index(request):
    # Verificar que el usuario autenticado es un empleado
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, 'No estás registrado como repartidor.')
        return redirect('dashboard')  # Redirige a una página adecuada

    # Obtener el perfil del empleado
    repartidor = request.user.employee_profile

    # Verificar que el empleado tiene el rol de repartidor
    if repartidor.id_rol.name != 'Repartidor':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')

    # Obtener pedidos asignados al repartidor
    pedidos = Order.objects.filter(id_employee=repartidor).exclude(id_status=5).order_by('order_date')

    # Calcular el total de cada pedido
    pedidos_con_totales = []
    for pedido in pedidos:
        total = pedido.id_cart.detail_set.aggregate(total=Sum('sub_total'))['total'] or 0
        pedidos_con_totales.append({
            'pedido': pedido,
            'total': total
        })

    return render(request, 'index.html', {
        'repartidor': repartidor,
        'pedidos_con_totales': pedidos_con_totales,
    })

def activar_repartidor(request):
    repartidor = get_object_or_404(Employee, user=request.user, id_rol=5)
    repartidor.is_active = True
    repartidor.save()
    messages.success(request, "Te has activado exitosamente.")
    return redirect('repartidores:index')

def desactivar_repartidor(request):
    repartidor = get_object_or_404(Employee, user=request.user, id_rol=5)
    repartidor.is_active = False
    repartidor.save()
    messages.success(request, "Te has desactivado exitosamente.")
    return redirect('repartidores:index')

def entregar_pedido(request, pedido_id):
    # Verificar que el usuario tiene un perfil de empleado asociado
    try:
        repartidor = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, "No estás registrado como repartidor.")
        return redirect('repartidores:index')

    # Obtener el pedido asignado al repartidor
    try:
        pedido = Order.objects.get(id_order=pedido_id, id_employee=repartidor)
    except Order.DoesNotExist:
        messages.error(request, "No tienes permiso para entregar este pedido o el pedido no existe.")
        return redirect('repartidores:index')

    # Actualizar el estado del pedido
    entregado_status = get_object_or_404(Order_status, id_status=5)  # Asegúrate de que este ID corresponde a "Entregado"
    pedido.id_status = entregado_status
    pedido.last_update = now()
    pedido.save()

    # Mensaje de éxito
    messages.success(request, f"El pedido #{pedido.id_order} se ha marcado como entregado.")
    return redirect('repartidores:index')
