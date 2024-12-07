from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages
from .models import Configuration, Cupon, Role, Employee, Customer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage


# configuration.


def GeneralView(request):
    return HttpResponse("Hello, world. You're at the index.")

# configuration.
def configuration_home(request):
    return render(request, 'configurations/configuracion_home.html')

def gestionar_configuraciones_view(request):
    return render(request, 'configurations/gestionar_configuraciones.html')

def gestionar_configuraciones(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        name = request.POST.get('name')
        address = request.POST.get('address')
        color_pallette = request.POST.get('color_pallette')
        isPointActive = request.POST.get('isPointActive') == "on"

        # Manejo de imágenes
        pathLogo = request.FILES.get('pathLogo')
        path_slogan = request.FILES.get('path_slogan')

        # Guardar imágenes en la carpeta static/img
        fs = FileSystemStorage(location='modulo_administracion/static/img')
        fs.save(pathLogo.name, pathLogo) if pathLogo else None
        fs.save(path_slogan.name, path_slogan) if path_slogan else None

        pathLogo_url = f'modulo_administracion/static/img/{pathLogo.name}' if pathLogo else None
        path_slogan_url = f'modulo_administracion/static/img/{path_slogan.name}' if path_slogan else None

        # Crear nueva configuración
        configuracion = Configuration.objects.create(
            name=name,
            address=address,
            color_pallette=color_pallette,
            pathLogo=pathLogo_url,
            path_slogan=path_slogan_url,
            isPointActive=isPointActive
        )
        messages.success(request, f'Configuración {configuracion.name} creada exitosamente')
        return redirect('gestionar_configuraciones_view')

    else:
        # Si es un GET, retornar las configuraciones existentes
        configuraciones = Configuration.objects.all().order_by('-id')
        return JsonResponse(list(configuraciones.values()), safe=False)

def editar_configuracion(request, configuracion_id):
    configuracion = get_object_or_404(Configuration, id=configuracion_id)

    if request.method == 'POST':
        # Actualizar campos
        configuracion.name = request.POST.get('name')
        configuracion.address = request.POST.get('address')
        configuracion.color_pallette = request.POST.get('color_pallette')
        configuracion.isPointActive = request.POST.get('isPointActive') == "on"

        # Manejo de imágenes
        if 'pathLogo' in request.FILES:
            fs = FileSystemStorage(location='modulo_administracion/static/img')
            configuracion.pathLogo = fs.save(request.FILES['pathLogo'].name, request.FILES['pathLogo'])
        if 'path_slogan' in request.FILES:
            fs = FileSystemStorage(location='modulo_administracion/static/img')
            configuracion.path_slogan = fs.save(request.FILES['path_slogan'].name, request.FILES['path_slogan'])

        configuracion.save()
        messages.success(request, f'Configuración {configuracion.name} actualizada exitosamente')
        return redirect('gestionar_configuraciones_view')

    # Retornar configuración como JSON
    return JsonResponse({
        "id": configuracion.id,
        "name": configuracion.name,
        "address": configuracion.address,
        "color_pallette": configuracion.color_pallette,
        "pathLogo": configuracion.pathLogo,
        "path_slogan": configuracion.path_slogan,
        "isPointActive": configuracion.isPointActive
    })

def eliminar_configuracion(request, configuracion_id):
    configuracion = get_object_or_404(Configuration, id=configuracion_id)
    configuracion.delete()
    messages.success(request, f'Configuración {configuracion.name} eliminada exitosamente')
    return redirect('gestionar_configuraciones_view')

def gestionar_cupones_view(request):
    return render(request, 'configurations/gestionar_cupones.html')


def gestionar_cupones(request):
    if request.method == 'POST':
        # Recibir los datos del formulario
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion')
        tipo_descuento = request.POST.get('tipo_descuento')
        valor_descuento = request.POST.get('valor_descuento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        uso_maximo = request.POST.get('uso_maximo')

        # Crear el nuevo cupón
        cupon = Cupon.objects.create(
            codigo=codigo,
            descripcion=descripcion,
            tipo_descuento=tipo_descuento,
            valor_descuento=valor_descuento,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            uso_maximo=uso_maximo
        )
        messages.success(request, f'Cupón {cupon.codigo} creado exitosamente')
        return redirect('gestionar_cupones_view')

    else:
        # Si es un GET, solo mostrar la página sin cambiar nada
        cupones = Cupon.objects.all().order_by('-fecha_vencimiento')
        return JsonResponse(list(cupones.values()), safe=False)



def desactivar_cupon(request, cupon_id, flag):
    cupon = get_object_or_404(Cupon, id=cupon_id)
    if flag == 1:
        cupon.activo = True
        cupon.save()
        messages.success(request, f'Cupón {cupon.codigo} activado exitosamente')
        return JsonResponse({'estado': 'activado', 'codigo': cupon.codigo, 'message': f'Cupón {cupon.codigo} activado'})
    else:
        cupon.activo = False
        cupon.save()
        messages.success(request, f'Cupón {cupon.codigo} desactivado exitosamente')
        return JsonResponse({'estado': 'desactivado', 'codigo': cupon.codigo, 'message': f'Cupón {cupon.codigo} desactivado'})

def eliminar_cupon(request, cupon_id):
    cupon = get_object_or_404(Cupon, id=cupon_id)
    cupon.delete()
    messages.success(request, f'Cupón {cupon.codigo} eliminado exitosamente')
    return redirect('gestionar_cupones_view')

###################### CRUD ROLES #######################
def roles(request):
    return render(request, 'roles/roles.html')

def list_roles(request): #lista todos los roles
    roles = Role.objects.all()
    return render(request, 'roles/list_roles.html', {'roles': roles})

def list_roles_partial(request): #carga dinámicamente la lista de roles
    roles = Role.objects.all()
    return render(request, 'roles/list_roles.html', {'roles': roles})

#@login_required
def create_role(request): #crea un nuevo rol
    if request.method == 'POST':
        role = Role(name = request.POST['name'])
        role.save()
        messages.success(request, "Rol creado correctamente.")
        return redirect('roles')
    else:
        return render(request, 'roles/create_role.html')

def create_role_partial(request): #crea un nuevo rol dentro de un formulario dinámico
    if request.method == 'POST':
        role = Role(name = request.POST['name'])
        role.save()
        messages.success(request, "Rol creado correctamente.")
        return redirect('roles')
    else:
        return render(request, 'roles/create_role.html')

#@login_required
def edit_role(request, id): #edita un rol existente
    role = get_object_or_404(Role, id = id)
    if request.method == 'POST':
        role.name = request.POST['name']
        role.save()
        messages.success(request, "Rol actualizado correctamente.")
        return redirect('roles')
    else:
        return render(request, 'roles/edit_role.html', {'role': role})

#@login_required
def delete_role(request, id): #borra un rol existente
    role = get_object_or_404(Role, id = id)
    role.delete()
    messages.success(request, "Rol eliminado correctamente.")
    return redirect('roles')


###################### CRUD EMPLOYEES #######################
def employees(request):
    return render(request, 'employees/employees.html')

def list_employees(request): #lista todos los empleados
    employees = Employee.objects.all()
    return render(request, 'employees/list_employees.html', {'employees': employees})

def list_employees_partial(request): #carga dinámicamente la lista de empleados
    employees = Employee.objects.all()
    return render(request, 'employees/list_employees.html', {'employees': employees})

#@login_required
def create_employee(request): #crea un nuevo empleado
    roles = Role.objects.all()  # Obtiene todos los roles

    if request.method == 'POST':
        # Convierte el valor del POST 'id_role' a un objeto Role
        role_id = request.POST['id_role']
        role = Role.objects.get(id=role_id) 

        employee = Employee(
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            username=request.POST['username'],
            password=request.POST['password'],
            isActive=request.POST['isActive'],
            id_role=role,  # Asigna la instancia de Role
        )
        employee.save()
        messages.success(request, "Empleado creado correctamente.")
        return redirect('employees')
    else:
        return render(request, 'employees/create_employee.html', {'roles': roles})

#@login_required
def create_employee_partial(request): #crea un nuevo empleado dentro de un formulario dinámico
    roles = Role.objects.all()  # Obtiene todos los roles
    
    if request.method == 'POST':
        # Convierte el valor del POST 'id_role' a un objeto Role
        role_id = request.POST['id_role']
        role = Role.objects.get(id=role_id)
        
        employee = Employee(
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            username=request.POST['username'],
            password=request.POST['password'],
            isActive=request.POST['isActive'],
            id_role=role,  # Asigna la instancia de Role
        )
        employee.save()
        messages.success(request, "Empleado creado correctamente.")
        return redirect('employees')
    else:
        return render(request, 'employees/create_employee.html', {'roles': roles})

#@login_required
def edit_employee(request, id): #edita un empleado existente
    employee = get_object_or_404(Employee, id = id)
    roles = Role.objects.all()  # Obtiene todos los roles
    
    if request.method == 'POST':
        role_id = request.POST['id_role']
        role = Role.objects.get(id=role_id)

        employee.firstname = request.POST['firstname']
        employee.lastname = request.POST['lastname']
        employee.username = request.POST['username']
        employee.password = request.POST['password']
        employee.isActive = request.POST['isActive']
        employee.id_role = role  # Asigna la instancia de Role en vez del id
        employee.save()

        messages.success(request, "Empleado actualizado correctamente.")
        return redirect('employees')
    else:
        return render(request, 'employees/edit_employee.html', {'employee': employee, 'roles': roles})

#@login_required
def delete_employee(request, id): #borra un empleado existente
    employee = get_object_or_404(Employee, id = id)
    employee.delete()
    messages.success(request, "Empleado eliminado correctamente.")
    return redirect('employees')


###################### CRUD CUSTOMERS #######################
def customers(request):
    return render(request, 'customers/customers.html')

def list_customers(request): #lista todos los consumidores/clientes
    customers = Customer.objects.all()
    return render(request, 'customers/list_customers.html', {'customers': customers})

def list_customers_partial(request): #carga dinámicamente la lista de clientes
    customers = Customer.objects.all()
    return render(request, 'customers/list_customers.html', {'customers': customers})

#@login_required
def create_customer(request): #crea un nuevo consumidor/cliente
    if request.method == 'POST':
        customer = Customer(firstname = request.POST['firstname'], 
                            lastname = request.POST['lastname'], 
                            user = request.POST['user'], 
                            password = request.POST['password']
                            #idConfiguration = request.POST['idConfiguration']
                            )
        customer.save()
        messages.success(request, "Cliente creado correctamente.")
        return redirect('customers')
    else:
        return render(request, 'customers/create_customer.html')

#@login_required
def create_customer_partial(request): #crea un nuevo consumidor/cliente dentro de un formulario dinámico
    if request.method == 'POST':
        customer = Customer(firstname = request.POST['firstname'], 
                            lastname = request.POST['lastname'], 
                            user = request.POST['user'], 
                            password = request.POST['password']
                            #idConfiguration = request.POST['idConfiguration']
                            )
        customer.save()
        messages.success(request, "Cliente creado correctamente.")
        return redirect('customers')
    else:
        return render(request, "customers/create_customer.html")

#@login_required
def edit_customer(request, id): #edita un consumidor/cliente existente
    customer = get_object_or_404(Customer, id = id)
    if request.method == 'POST':
        customer.firstname = request.POST['firstname']
        customer.lastname = request.POST['lastname']
        customer.user = request.POST['user']
        customer.password = request.POST['password']
        #customer.idConfiguration = request.POST['idConfiguration']
        customer.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect('customers')
    else:
        return render(request, 'customers/edit_customer.html', {'customer': customer})

#@login_required
def edit_customer_partial(request, id): #carga dinámicamente el formulario de edición de cliente
    customer = get_object_or_404(Customer, id = id)
    if request.method == 'POST':
        customer.firstname = request.POST['firstname']
        customer.lastname = request.POST['lastname']
        customer.user = request.POST['user']
        customer.password = request.POST['password']
        #customer.idConfiguration = request.POST['idConfiguration']
        customer.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect('customers')
    else:
        return render(request, 'customers/edit_customer.html', {'customer': customer})

#@login_required
def delete_customer(request, id): #borra un consumidor/cliente existente    
    customer = get_object_or_404(Customer, id = id)
    customer.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('customers')
