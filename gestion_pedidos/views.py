from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from .models import ShoppingCart, Departamento, Municipio, Distrito, Detail, CustomerAddress
from moduloDespacho.models import Order_status, Order
from modulo_catalogo.models import Product
from modulo_administracion.models import Customer, Employee, Role, Cupon
import json



# Vista principal para mostrar pedidos recientes
def order_list(request):
    orders = Order.objects.all().order_by('order_date')[:10]  # Obtener los pedidos más recientes
    return render(request, 'gestion_pedido/order_list.html', {'orders': orders})

# Vista para crear un nuevo pedido
def order_create(request):
    if request.method == 'POST':
        # Validar datos del formulario
        customer_id = request.POST.get('customer_id')
        id_departamento = request.POST.get('id_departamento')
        id_distrito = request.POST.get('id_distrito')
        address_detail = request.POST.get('address', '')
        products_data = request.POST.get('products_data') 

        print(request.POST)
        print(customer_id)

        # Verificar que todos los datos necesarios estén presentes
        if not customer_id:
            messages.error(request, 'Por favor selecciona un cliente.')
            return redirect('order_create')
        if not id_departamento or not id_distrito:
            messages.error(request, 'Por favor selecciona un departamento y un distrito.')
            return redirect('order_create')

        # Obtener o crear objetos relacionados
        customer = get_object_or_404(Customer, id_customer=customer_id)
        distrito = get_object_or_404(Distrito, id_distrito=id_distrito)

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
        shopping_cart = ShoppingCart.objects.create(customer=customer)

        # Verificar cupón (si aplica)
        coupon_code = request.POST.get('coupon_code', None)
        coupon = None
        if coupon_code:
            coupon = Cupon.objects.filter(coupon_code=coupon_code).first()
        
        # Procesar productos y agregar al carrito
        import json
        if not products_data:
            messages.error(request, 'No se recibieron productos. Por favor selecciona al menos un producto.')
            return redirect('order_create')

        try:
            products = json.loads(products_data)
            if not products:
                raise ValueError("No hay productos seleccionados.")
        except json.JSONDecodeError:
            messages.error(request, 'Los datos de los productos son inválidos.')
            return redirect('order_create')

        # Crear detalles para cada producto
        for product in products:
            product_instance = get_object_or_404(Product, id_product=product['id'])
            quantity = int(product['quantity'])
            subtotal = float(product['subtotal'])

            # Reducir stock del producto
            product_instance.count -= quantity
            product_instance.save()

            # Crear el detalle en el carrito
            Detail.objects.create(
                shoppingcart=shopping_cart,
                product=product_instance,
                amount=quantity,
                sub_total=subtotal
            )

        # Crear pedido
        order_status = get_object_or_404(Order_status, id_status=1)
        # Filtrar empleados activos con el rol de repartidor
        repartidor_role = get_object_or_404(Role, name='Repartidor')  # Asegúrate de que este rol existe
        available_employee = Employee.objects.filter(is_active=True, id_rol=repartidor_role).first()

        if not available_employee:
            messages.error(request, 'No hay empleados disponibles con el rol de repartidor.')
            return redirect('order_create')  # Redirige a la página de creación con un mensaje de error

        order = Order.objects.create(
            id_cart=shopping_cart,
            id_address=customer_address,  # Ahora es una instancia de CustomerAddress
            id_cupon=coupon,            
            id_employee=available_employee,
            id_status=order_status,
            order_date=now(),
        )

        messages.success(request, f'Pedido #{order.id_order} creado exitosamente.')
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
def buscar_municipios(request, Id_departamento):
    if request.method == 'GET':
        departamento = Departamento.objects.filter(id_departamento=Id_departamento).first()
        
        municipios = Municipio.objects.filter(id_departamento=departamento.id_departamento).values('id_municipio', 'name')
    return JsonResponse({'municipios': list(municipios)})

# Buscar distritos según municipio
def buscar_distritos(request, id_municipio):
    distritos = Distrito.objects.filter(id_municipio=id_municipio).values('id_distrito', 'name')
    return JsonResponse({'distritos': list(distritos)})

# Buscar productos por nombre
def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)
    return JsonResponse({'products': list(products.values('id_product', 'name', 'price', 'count'))})

# Buscar clientes por nombre
def search_customers(request):
    query = request.GET.get('query', '')
    customers = Customer.objects.filter(firstName__icontains=query)
    return JsonResponse({'customers': list(customers.values('id_customer', 'firstName', 'lastName'))})

# Validar cupón
def validar_cupon(request):
    code = request.GET.get('code', '')
    try:
        coupon = Cupon.objects.get(coupon_code=code)
        # Verificar si el cupón está expirado
        if coupon.exp_date <= now():  # Utilizamos timezone.now() para fechas aware
            return JsonResponse({'valid': False, 'message': 'El cupón ha expirado y no es válido.'})
        
        # Si el cupón es válido, desactivarlo
        coupon.exp_date = now()  # Cambiar la fecha de expiración a la actual
        coupon.save()
        return JsonResponse({'valid': True, 'discount': coupon.coupon_discount})
    except Cupon.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Cupón inválido o no encontrado.'})

def get_registered_address(request):
    customer_id = request.GET.get('id_customer')

    # Verificar que se envió un cliente
    if not customer_id:
        return JsonResponse({'error': 'No se proporcionó un cliente.'}, status=400)

    # Buscar la dirección del cliente
    customer = get_object_or_404(Customer, id_customer=customer_id)
    customer_address = customer.customeraddress_set.first()

    if not customer_address:
        return JsonResponse({'error': 'El cliente no tiene una dirección registrada.'}, status=400)

    # Devolver la dirección en formato JSON
    return JsonResponse({
        'id_departamento_': customer_address.Distrito.municipio.departamento.id_departamento,
        'id_municipio': customer_address.Distrito.municipio.id_municipio,
        'id_distrito': customer_address.Distrito.id_distrito,
        'address_detail': customer_address.address
    })

# Editar order
def order_edit(request, order_id):
    # Obtener el pedido
    order = get_object_or_404(Order, id=order_id)

    # Manejar el formulario de edición
    if request.method == 'POST':
        # Dirección
        id_distrito = request.POST.get('id_distrito')
        address_detail = request.POST.get('address')
        if not id_distrito or not address_detail:
            messages.error(request, 'Por favor, completa todos los campos de dirección.')
            return redirect('order_edit', order_id=order_id)

        # Obtener el distrito y actualizar la dirección
        distrito = get_object_or_404(Distrito, id=id_distrito)
        customer_address, _ = CustomerAddress.objects.get_or_create(
            customer=order.shoppingcart.customer,
            Distrito=distrito,
            defaults={'address': address_detail}
        )
        order.address = customer_address

        # Repartidor
        repartidor_id = request.POST.get('repartidor_id')
        if repartidor_id:
            repartidor_role = get_object_or_404(Role, name='Repartidor')  # Asegúrate de tener este rol
            repartidor = get_object_or_404(Employee, id=repartidor_id, id_rol=repartidor_role, is_active=True)
            order.employee = repartidor

        # Guardar cambios
        order.save()
        messages.success(request, f'Pedido #{order.id} actualizado exitosamente.')
        return redirect('order_create')

    # Obtener datos para mostrar en el formulario
    distritos = Distrito.objects.all()
    repartidor_role = get_object_or_404(Role, name='Repartidor')  # Filtrar empleados por rol
    repartidores = Employee.objects.filter(id_rol=repartidor_role, is_active=True)

    return render(request, 'gestion_pedido/edit_order.html', {
        'order': order,
        'distritos': distritos,
        'repartidores': repartidores,
    })

def order_detail(request, order_id):
    # Obtener el pedido y sus detalles
    order = get_object_or_404(Order, id_order=order_id)
    details = Detail.objects.filter(shoppingcart=order.id_cart)

    # Calcular el total
    total = sum(detail.sub_total for detail in details)

    return render(request, 'gestion_pedido/detail_order.html', {
        'order': order,
        'details': details,
        'total': total,  # Pasar el total al contexto
    })
def dashboard(request):
    orders = Order.objects.all().order_by('order_date')
    return render(request, 'dashboard.html', {'orders': orders})
