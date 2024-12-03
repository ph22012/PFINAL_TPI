from django.shortcuts import render
from .models import Order
from datetime import date
# Create your views here.
#logica de la vista de despachos    
def mostrar_ordenes(request):
    ordenesP = Order.objects.filter(order_date = fechaHoy)

    return render (request,{'ordenesP':ordenesP})

def fechaHoy ():
    today = date.today()
    return today
