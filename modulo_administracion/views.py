from django.shortcuts import render

# Create your views here.
def GeneralView(request):
    return render(request, 'administracion/inicio.html')

def configuration(request):
    return render(request, 'administracion/configuracion.html')

def roles(request):
    return render(request, 'administracion/roles.html')

def employees(request):
    return render(request, 'administracion/empleados.html')

def customers(request):
    return render(request, 'administracion/customers.html')


