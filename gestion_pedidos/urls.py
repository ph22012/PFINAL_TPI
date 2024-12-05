from django.urls import path
from . import views

urlpatterns = [
    path('crear/buscar-clientes/', views.search_customers, name='search_customers'),  # Ruta para buscar clientes
    path('crear/buscar-productos/', views.search_products, name='search_products'),  # Ruta para buscar productos
    path('crear/buscar-municipios/<int:departamento_id>/', views.buscar_municipios, name='buscar_municipios'),  # Municipios
    path('crear/buscar-distritos/<int:municipio_id>/', views.buscar_distritos, name='buscar_distritos'),  # Distritos
    path('crear/validar-cupon/', views.validar_cupon, name='validar_cupon'),  # Validar cupón
    path('get-registered-address/', views.get_registered_address, name='get_registered_address'),
    path('crear/', views.order_create, name='order_create'),  # Crear pedido
    path('', views.order_list, name='order_list'),  # Lista de pedidos
]
