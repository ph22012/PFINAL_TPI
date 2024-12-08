from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from modulo_catalogo.models import Product

# Create your views here.
def index(request):
    return render(request, 'indexCata.html')  # Renderiza la plantilla principal

def catalogo_productos(request):
    return render(request, 'catalogo_productos/catalogoDeProductos.html')  # Renderiza la plantilla de catalogo de productos

def logout_view(request):
    return render(request, 'index.html')  # Renderiza la plantilla principal

def menu_diario(request):
    return render(request, 'menu/menuDelDia.html')  # Renderiza la plantilla de menu del dia

#-------------------------------------------------------------------------------
# Vista para eliminar un producto
"""def eliminar_producto(request):
    if request.method == "POST":
        # Obtener el ID del producto enviado desde el formulario
        product_id = request.POST.get('productId')

        if not product_id:
            return HttpResponse("El ID del producto no puede estar vacío.", status=400)

        # Buscar el producto por ID
        producto = get_object_or_404(Product, id_product=product_id)

        # Eliminar el producto
        producto.delete()

        # Redirigir a la página del catálogo o a otra vista con un mensaje de éxito
        return redirect('catalogo_productos')  # O cualquier vista de éxito

    return render(request, 'delete_product_template.html')  # Renderiza la plantilla de eliminación"""
def eliminar_producto(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = get_object_or_404(Product, id_product=product_id)
            product.delete()
            return redirect('catalogo_productos')  # Redirige al catálogo después de eliminar
        except:
            return HttpResponse("El producto no se pudo encontrar o eliminar.")
    return render(request, 'catalogo_productos/catalogoDeProductos.html')

def agregar_producto(request):
    if request.method == 'POST':
        # Lógica para agregar productos al catálogo
        # Aquí podrías procesar el ID de los productos recibidos en la petición AJAX
        # Ejemplo de cómo agregar un producto (simplificado)
        producto = Product.objects.create(
            name=request.POST['nombre'],
            id_category=request.POST['categoria'],
            price=request.POST['precio'],
            description=request.POST['descripcion'],
            count=request.POST['cantidad'],
        )
        return JsonResponse({"mensaje": "Producto agregado correctamente"})
    return render(request, 'catalogo_productos/agregar.html')