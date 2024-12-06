from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')  # Renderiza la plantilla principal

def catalogo_productos(request):
    return render(request, 'catalogo_productos/catalogoDeProductos.html')  # Renderiza la plantilla de catalogo de productos

def logout_view(request):
    return render(request, 'index.html')  # Renderiza la plantilla principal

def menu_diario(request):
    return render(request, 'menu/menuDelDia.html')  # Renderiza la plantilla de menu del dia