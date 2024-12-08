from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages
from .models import Configuration, Cupon, RewardPoints, Role, Employee, Customer, CustomUser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
import os


# configuration.


def GeneralView(request):
    return render(request, 'home.html')

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
        color_pallette_bg = request.POST.get('color_pallette_bg')
        isPointActive = request.POST.get('isPointActive') == "on"

        # Manejo de imágenes
        pathLogo = request.FILES.get('pathLogo')
        path_slogan = request.FILES.get('path_slogan')

        # Guardar imágenes en la carpeta static/img
        fs = FileSystemStorage(location='modulo_administracion/static/img')
        fs.save(pathLogo.name, pathLogo) if pathLogo else None
        fs.save(path_slogan.name, path_slogan) if path_slogan else None

        pathLogo_url = f'{pathLogo.name}' if pathLogo else None
        path_slogan_url = f'{path_slogan.name}' if path_slogan else None

        # Crear nueva configuración
        configuracion = Configuration.objects.create(
            name=name,
            address=address,
            color_pallette=color_pallette,
            color_pallette_bg=color_pallette_bg,
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
    fs = FileSystemStorage(location='modulo_administracion/static/img')

    if request.method == 'POST':
        # Actualizar campos del formulario
        configuracion.name = request.POST.get('name', configuracion.name)
        configuracion.address = request.POST.get('address', configuracion.address)
        configuracion.color_pallette = request.POST.get('color_pallette', configuracion.color_pallette)
        configuracion.color_pallette_bg = request.POST.get('color_pallette_bg', configuracion.color_pallette_bg)
        configuracion.isPointActive = request.POST.get('isPointActive') == "on"

        # Manejo de logo
        if request.POST.get('deleteLogo') == 'true':  # Si el usuario quiere eliminar el logo actual
            if configuracion.pathLogo and os.path.exists(fs.path(configuracion.pathLogo)):
                os.remove(fs.path(configuracion.pathLogo))
            configuracion.pathLogo = None
        elif 'pathLogo' in request.FILES:  # Si sube un nuevo archivo de logo
            if configuracion.pathLogo and os.path.exists(fs.path(configuracion.pathLogo)):
                os.remove(fs.path(configuracion.pathLogo))  # Elimina el archivo antiguo
            configuracion.pathLogo = fs.save(request.FILES['pathLogo'], request.FILES['pathLogo'])

        # Manejo de slogan
        if request.POST.get('deleteSlogan') == 'true':  # Si el usuario quiere eliminar el slogan actual
            if configuracion.path_slogan and os.path.exists(fs.path(configuracion.path_slogan)):
                os.remove(fs.path(configuracion.path_slogan))
            configuracion.path_slogan = None
        elif 'path_slogan' in request.FILES:  # Si sube un nuevo archivo de slogan
            if configuracion.path_slogan and os.path.exists(fs.path(configuracion.path_slogan)):
                os.remove(fs.path(configuracion.path_slogan))  # Elimina el archivo antiguo
            configuracion.path_slogan = fs.save(request.FILES['path_slogan'], request.FILES['path_slogan'])

        configuracion.save()
        messages.success(request, f'Configuración {configuracion.name} actualizada exitosamente')
        return JsonResponse({'success': True, 'message': 'Configuración actualizada con éxito.'})

    else:
        # Retornar configuración como JSON para edición
        return JsonResponse({
            "id": configuracion.id,
            "name": configuracion.name,
            "address": configuracion.address,
            "color_pallette": configuracion.color_pallette,
            "color_pallette_bg": configuracion.color_pallette_bg,
            "pathLogo": configuracion.pathLogo if configuracion.pathLogo else "",
            "path_slogan": configuracion.path_slogan if configuracion.path_slogan else "",
            "isPointActive": configuracion.isPointActive,
        })


def eliminar_configuracion(request, configuracion_id):
    fs = FileSystemStorage(location='modulo_administracion/static/img')
    configuracion = get_object_or_404(Configuration, id=configuracion_id)
    print(f'Eliminando configuración {configuracion.pathLogo}')
    print(f'Eliminando configuración {configuracion.path_slogan}')
    # Eliminar archivos de imágenes
    if configuracion.pathLogo and os.path.exists(fs.path(configuracion.pathLogo)):
        print("Existe este path")
        os.remove(fs.path(configuracion.pathLogo))
    if configuracion.path_slogan and os.path.exists(fs.path(configuracion.path_slogan)):
        os.remove(fs.path(configuracion.path_slogan))

    configuracion.delete()
    messages.success(request, f'Configuración {configuracion.name} eliminada exitosamente')
    return redirect('gestionar_configuraciones_view')

def aplicar_configuracion(request, configuracion_id):
    configuracion = get_object_or_404(Configuration, id=configuracion_id)
    return JsonResponse({
            "id": configuracion.id,
            "name": configuracion.name,
            "address": configuracion.address,
            "color_pallette": configuracion.color_pallette,
            "color_pallette_bg": configuracion.color_pallette_bg,
            "pathLogo": configuracion.pathLogo if configuracion.pathLogo else "",
            "path_slogan": configuracion.path_slogan if configuracion.path_slogan else "",
            "isPointActive": configuracion.isPointActive,
        })

###################### CRUD CUPONES #######################

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
        
        #Captura los datos del formulario
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        password=request.POST['password']
        isActive=request.POST['isActive']
          
        #Crea el empleado, primero con customUser
        if CustomUser.objects.filter(username=username).exists():
           print('El usuario ya existe')
           return redirect('employees')
        else:
            user = CustomUser.objects.create_user(username=username, password=password, is_employee=True)
            empleado = Employee.objects.create(user=user, firstName=firstname, lastName=lastname, is_active=isActive, id_rol=role)
            empleado.save()
            messages.success(request, "Empleado creado correctamente.")
            return redirect('employees')
    else:
        return render(request, 'employees/create_employee.html', {'roles': roles})

#@login_required
def edit_employee(request, id): #edita un empleado existente
    employee = get_object_or_404(Employee, id_employee = id)
    roles = Role.objects.all()  # Obtiene todos los roles
    
    if request.method == 'POST':
        role_id = request.POST['id_role']
        role = Role.objects.get(id=role_id)

        employee.firstName = request.POST['firstname']
        employee.lastName = request.POST['lastname']
        employee.user.username = request.POST['username']
        employee.user.set_password = request.POST['password']
        employee.is_active = request.POST['isActive']
        employee.id_rol = role  # Asigna la instancia de Role en vez del id
        employee.save()

        messages.success(request, "Empleado actualizado correctamente.")
        return redirect('employees')
    else:
        return render(request, 'employees/edit_employee.html', {'employee': employee, 'roles': roles})

#@login_required
def delete_employee(request, id): #borra un empleado existente
    employee = get_object_or_404(Employee, id_employee = id)
    employee.user.delete()
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
        puntos = RewardPoints.objects.get(id=1)
        customUser = CustomUser.objects.create_user( 
                            username = request.POST['user'],
                            password = request.POST['password'],
                            is_customer = True,
                            #idConfiguration = request.POST['idConfiguration']
                            )
        #customer.save()
        Customer.objects.create(user = customUser, firstName = request.POST['firstname'], 
                            lastName = request.POST['lastname'], id_points = puntos)
        messages.success(request, "Cliente creado correctamente.")
        return redirect('customers')
    else:
        return render(request, "customers/create_customer.html")

#@login_required
def create_customer_partial(request): #crea un nuevo consumidor/cliente dentro de un formulario dinámico
    
    if request.method == 'POST':
        if CustomUser.objects.filter(username=request.POST['user']).exists():
            print('El usuario ya existe')
            return redirect('customers')
        else:
            puntos = RewardPoints.objects.create(exp_date=now(), points_count=0)
            customUser = CustomUser.objects.create_user( 
                            username = request.POST['user'],
                            password = request.POST['password'],
                            is_customer = True,
                            #idConfiguration = request.POST['idConfiguration']
                            )
        #customer.save()
            Customer.objects.create(user = customUser, firstName = request.POST['firstname'], 
                            lastName = request.POST['lastname'], id_points = puntos)
        messages.success(request, "Cliente creado correctamente.")
        return redirect('customers')
    else:
        return render(request, "customers/create_customer.html")

#@login_required
def edit_customer(request, id): #edita un consumidor/cliente existente
    customer = get_object_or_404(Customer, id_customer = id)
    if request.method == 'POST':
        customer.firstName = request.POST['firstname']
        customer.lastName = request.POST['lastname']
        customer.user.username = request.POST['user']
        contraseña = request.POST['password']
        customer.user.set_password(contraseña)
        #customer.idConfiguration = request.POST['idConfiguration']
        customer.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect('customers')
    else:
        return render(request, 'customers/edit_customer.html', {'customer': customer})

#@login_required
def edit_customer_partial(request, id): #carga dinámicamente el formulario de edición de cliente
    customer = get_object_or_404(Customer, id_customer = id)
    if request.method == 'POST':
        customer.firstName = request.POST['firstname']
        customer.lastName = request.POST['lastname']
        customer.user.username = request.POST['user']
        contraseña = request.POST['password']
        customer.user.set_password(contraseña)
        #customer.idConfiguration = request.POST['idConfiguration']
        customer.user.save()
        customer.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect('customers')
    else:
        return render(request, 'customers/edit_customer.html', {'customer': customer})

#@login_required
def delete_customer(request, id): #borra un consumidor/cliente existente    
    customer = get_object_or_404(Customer, id_customer = id)
    customer.user.delete()
    customer.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('customers')
