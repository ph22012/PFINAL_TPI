from django.shortcuts import render
from .models import Order

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'moduloDespacho/Orders.html', {'orders': orders})
