from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages
from .models import Configuration, Cupon, Role, Employee, Customer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# configuration.


def GeneralView(request):
    return HttpResponse("Hello, world. You're at the index.")

# configuration.
def configuration_home(request):
    return render(request, 'configurations/configuracion_home.html')

    
class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ['name', 'pathLogo', 'path_slogan', 'color_pallette', 'address', 'isPointActive']
        widgets = {
            'Nombre de la configuración': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la configuración'}),
            'Ruta del logo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ruta del logo'}),
            'Ruta del eslogan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ruta del eslogan'}),
            'Paleta de colores': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paleta de colores'}),
            'Dirección': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'Activar el programa de puntos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class ConfigurationUpdateView(UpdateView):
    model = Configuration
    form_class = ConfigurationForm
    template_name = 'configurations/configuration_form.html'
    success_url = reverse_lazy('admin_home')

    def form_valid(self, form):
        instance = form.save(commit=False)
        if not instance.isPointActive:
            messages.info(self.request, "El programa de puntos ha sido desactivado. Los puntos actuales no se perderán.")
        else:
            messages.success(self.request, "El programa de puntos ha sido activado con éxito.")
        instance.save()
        return super().form_valid(form)



##cupones

def gestionar_cupones(request):
    cupones = Cupon.objects.all().order_by('-fecha_vencimiento')

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion')
        tipo_descuento = request.POST.get('tipo_descuento')
        valor_descuento = request.POST.get('valor_descuento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        uso_maximo = request.POST.get('uso_maximo')

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
        return redirect('gestionar_cupones')

    return render(request, 'configurations/gestionar_cupones.html', {
        'cupones': cupones
    })


def desactivar_cupon(request, cupon_id):
    cupon = get_object_or_404(Cupon, id=cupon_id)
    cupon.activo = False
    cupon.save()
    messages.success(request, f'Cupón {cupon.codigo} desactivado')
    return redirect('gestionar_cupones')


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
    return render(request, 'employees/employees.html')

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

def list_customers_partial(request): #carga dinámicamente la lista de clientes
    customers = Customer.objects.all()
    print("algo") 
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
        messages.success(request, "Cliente creado correctamente.")
        return redirect('customers')
    else:
        return render(request, 'customers/create_customer.html')

@login_required
def create_customer_partial(request):
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
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect('customers')
    else:
        return render(request, 'customers/edit_customer.html', {'customer': customer})

@login_required
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

@login_required
def delete_customer(request, id): #borra un consumidor/cliente existente    
    customer = get_object_or_404(Customer, id = id)
    customer.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('customers')
