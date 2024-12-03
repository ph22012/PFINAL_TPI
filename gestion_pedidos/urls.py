from django.urls import path
from . import views

urlpatterns = [
    path("pedidos/", views.gestion_pedidos, name="pedidos"),
    path("pedidos/crear/", views.crear_pedido, name="crear_pedido"),
    path("pedidos/modificar/<int:pedido_id>/", views.modificar_pedido, name="modificar_pedido"),
    path("pedidos/cancelar/<int:pedido_id>/", views.cancelar_pedido, name="cancelar_pedido"),
]
