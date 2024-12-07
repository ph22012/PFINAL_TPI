from django.urls import path
from . import views

app_name = 'repartidores'

urlpatterns = [
    path('', views.repartidores_index, name='index'),
    path('activar/', views.activar_repartidor, name='activar'),
    path('desactivar/', views.desactivar_repartidor, name='desactivar'),
    path('entregar/<int:pedido_id>/', views.entregar_pedido, name='entregar'),
]