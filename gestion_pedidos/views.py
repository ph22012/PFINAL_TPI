from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import (
    Order, OrderStatus, Employee, ShoppingCart, Customer, Product, CustomerAddress,
    Departamento, Distrito, Coupon, Detail
)

# Vista principal para mostrar pedidos recientes
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')[:10]  # Obtener los pedidos más recientes
    return render(request, 'gestion_pedido/order_list.html', {'orders': orders})

# Vista para crear un nuevo pedido
def order_create(request):
    if request.method == 'POST':
        # Validar datos del formulario
        customer_id = request.POST.get('customer_id')
        departamento_id = request.POST.get('departamento_id')
        distrito_id = request.POST.get('distrito_id')
        address_detail = request.POST.get('address', '')

        # Verificar que todos los datos necesarios estén presentes
        if not customer_id:
            messages.error(request, 'Por favor selecciona un cliente.')
            return redirect('order_create')
        if not departamento_id or not distrito_id:
            messages.error(request, 'Por favor selecciona un departamento y un distrito.')
            return redirect('order_create')

        # Obtener o crear objetos relacionados
        customer = get_object_or_404(Customer, id=customer_id)
        distrito = get_object_or_404(Distrito, id=distrito_id)

        # Crear o usar una dirección registrada
        if 'use_registered_address' in request.POST:
            customer_address = CustomerAddress.objects.filter(customer=customer).first()
            if not customer_address:
                messages.error(request, 'El cliente no tiene una dirección registrada.')
                return redirect('order_create')
        else:
            # Crear una nueva dirección si no se usa la registrada
            customer_address, _ = CustomerAddress.objects.get_or_create(
                customer=customer,
                Distrito=distrito,
                defaults={'address': address_detail}
            )

        # Crear carrito si no existe
        shopping_cart, _ = ShoppingCart.objects.get_or_create(customer=customer)

        # Verificar cupón (si aplica)
        coupon_code = request.POST.get('coupon_code', None)
        coupon = None
        if coupon_code:
            coupon = Coupon.objects.filter(coupon_code=coupon_code).first()

        # Crear pedido
        order_status = get_object_or_404(OrderStatus, status='Pendiente')
        available_employee = Employee.objects.filter(is_active=True).first()

        order = Order.objects.create(
            shoppingcart=shopping_cart,
            address=customer_address,  # Ahora es una instancia de CustomerAddress
            coupon=coupon,
            status=order_status,
            employee=available_employee,
        )

        messages.success(request, f'Pedido #{order.id} creado exitosamente.')
        return redirect('order_create')

    # Obtener datos iniciales
    customers = Customer.objects.all()
    products = Product.objects.all()
    departamentos = Departamento.objects.all()
    return render(request, 'gestion_pedido/create_order.html', {
        'customers': customers,
        'products': products,
        'departamentos': departamentos,
    })


# Buscar municipios según departamento
def buscar_municipios(request, departamento_id):
    municipios = Distrito.objects.filter(municipio__departamento_id=departamento_id).values('id', 'name')
    return JsonResponse({'municipios': list(municipios)})

# Buscar distritos según municipio
def buscar_distritos(request, municipio_id):
    distritos = Distrito.objects.filter(municipio_id=municipio_id).values('id', 'name')
    return JsonResponse({'distritos': list(distritos)})

# Buscar productos por nombre
def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)
    return JsonResponse({'products': list(products.values('id', 'name', 'price', 'count'))})

# Buscar clientes por nombre
def search_customers(request):
    query = request.GET.get('query', '')
    customers = Customer.objects.filter(firstname__icontains=query)
    return JsonResponse({'customers': list(customers.values('id', 'firstname', 'lastname'))})

# Validar cupón
def validar_cupon(request):
    code = request.GET.get('code', '')
    try:
        coupon = Coupon.objects.get(coupon_code=code)
        return JsonResponse({'valid': True, 'discount': coupon.coupon_discount})
    except Coupon.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Cupón inválido o expirado.'})

def get_registered_address(request):
    customer_id = request.GET.get('customer_id')

    # Verificar que se envió un cliente
    if not customer_id:
        return JsonResponse({'error': 'No se proporcionó un cliente.'}, status=400)

    # Buscar la dirección del cliente
    customer = get_object_or_404(Customer, id=customer_id)
    customer_address = customer.customeraddress_set.first()

    if not customer_address:
        return JsonResponse({'error': 'El cliente no tiene una dirección registrada.'}, status=400)

    # Devolver la dirección en formato JSON
    return JsonResponse({
        'departamento_id': customer_address.Distrito.municipio.departamento.id,
        'municipio_id': customer_address.Distrito.municipio.id,
        'distrito_id': customer_address.Distrito.id,
        'address_detail': customer_address.address
    })
