from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.order_list, name='order_list'),
    path('get_datos_ordenes/', views.getOrdenes, name='get_datos_ordernes'),
]
