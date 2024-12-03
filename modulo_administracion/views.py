from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Configuration, Role, Employee, Customer

# Create your views here.


def GeneralView(request):
    return render(request, 'administracion/inicio.html')

def configuration(request):
    return render(request, 'administracion/configuracion.html')


###################### CRUD ROLES #######################
def roles(request):
    return render(request, 'roles/roles.html')

def list_roles(request): #lista todos los roles
    roles = Role.objects.all()
    return render(request, 'roles/list_roles.html', {'roles': roles})

@login_required
def create_role(request): #crea un nuevo rol
    if request.method == 'POST':
        role = Role(name = request.POST['name'])
        role.save()
        messages.success(request, "Rol creado correctamente.")
        return redirect('list_roles')
    else:
        return render(request, 'roles/create_role.html')

@login_required
def edit_role(request, id): #edita un rol existente
    role = get_object_or_404(Role, id = id)
    if request.method == 'POST':
        role.name = request.POST['name']
        role.save()
        messages.success(request, "Rol actualizado correctamente.")
        return redirect('list_roles')
    else:
        return render(request, 'roles/edit_role.html', {'role': role})

@login_required
def delete_role(request, id): #borra un rol existente
    role = get_object_or_404(Role, id = id)
    role.delete()
    messages.success(request, "Rol eliminado correctamente.")
    return redirect('list_roles')


###################### CRUD EMPLOYEES #######################
def employees(request):
    return render(request, 'employees/empleados.html')

def list_employees(request): #lista todos los empleados
    employees = Employee.objects.all()
    return render(request, 'employees/list_employees.html', {'employees': employees})

@login_required
def create_employee(request): #crea un nuevo empleado
    if request.method == 'POST':
        employee = Employee(firstname = request.POST['firstname'], 
                            lastname = request.POST['lastname'], 
                            username = request.POST['username'], 
                            password = request.POST['password'], 
                            isActive = request.POST['isActive'], 
                            id_role = request.POST['id_role'])
        employee.save()
        messages.success(request, "Empleado creado correctamente.")
        return redirect('list_employees')
    else:
        return render(request, 'employees/create_employee.html')

@login_required
def edit_employee(request, id): #edita un empleado existente
    employee = get_object_or_404(Employee, id = id)
    if request.method == 'POST':
        employee.firstname = request.POST['firstname']
        employee.lastname = request.POST['lastname']
        employee.username = request.POST['username']
        employee.password = request.POST['password']
        employee.isActive = request.POST['isActive']
        employee.id_role = request.POST['id_role']
        employee.save()
        messages.success(request, "Empleado actualizado correctamente.")
        return redirect('list_employees')
    else:
        return render(request, 'employees/edit_employee.html', {'employee': employee})

@login_required
def delete_employee(request, id): #borra un empleado existente
    employee = get_object_or_404(Employee, id = id)
    employee.delete()
    messages.success(request, "Empleado eliminado correctamente.")
    return redirect('list_employees')


###################### CRUD CUSTOMERS #######################
def customers(request):
    return render(request, 'customers/customers.html')

def list_customers(request): #lista todos los consumidores/clientes
    customers = Customer.objects.all()
    return render(request, 'customers/list_customers.html', {'customers': customers})

@login_required
def create_customer(request): #crea un nuevo consumidor/cliente
    if request.method == 'POST':
        customer = Customer(firstname = request.POST['firstname'], 
                            lastname = request.POST['lastname'], 
                            user = request.POST['user'], 
                            password = request.POST['password']
                            #idConfiguration = request.POST['idConfiguration']
                            )
        customer.save()
        messages.success(request, "Customer creado correctamente.")
        return redirect('list_customers')
    else:
        return render(request, 'customers/create_customer.html')

@login_required
def edit_customer(request, id): #edita un consumidor/cliente existente
    customer = get_object_or_404(Customer, id = id)
    if request.method == 'POST':
        customer.firstname = request.POST['firstname']
        customer.lastname = request.POST['lastname']
        customer.user = request.POST['user']
        customer.password = request.POST['password']
        #customer.idConfiguration = request.POST['idConfiguration']
        customer.save()
        messages.success(request, "Customer actualizado correctamente.")
        return redirect('list_customers')
    else:
        return render(request, 'customers/edit_customer.html', {'customer': customer})

@login_required
def delete_customer(request, id): #borra un consumidor/cliente existente    
    customer = get_object_or_404(Customer, id = id)
    customer.delete()
    messages.success(request, "Customer eliminado correctamente.")
    return redirect('list_customers')
