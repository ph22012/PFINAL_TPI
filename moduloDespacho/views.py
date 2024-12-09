from django.shortcuts import render 
from django.http import HttpResponse
from .models import Order
from datetime import date
import json

# Create your views here.
#logica de la vista de despachos    
def fechaHoy ():
    today = date.today()
    return today


def order_list(request):
    pendingOrders = Order.objects.filter(id_status__id_status=1).order_by('order_date')
    onProcessOrders = Order.objects.filter(id_status__id_status=2).order_by('last_update')
    return render(request, 'moduloDespacho/Orders.html',
    {'pendingOrders': pendingOrders, 'onProcessOrders': onProcessOrders})

def getOrdenes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print( "Datos: "+data)
    return HttpResponse("Datos obtenidos")
        