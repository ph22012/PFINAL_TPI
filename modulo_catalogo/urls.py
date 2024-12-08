from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index_catalogo, name='indexCatalogo'),
    path('logout/', views.logout_view, name='logout'),
    path('catalogo/', views.catalogo_productos, name='catalogo_productos'),
    path('menu/', views.menu_diario, name='menu_diario'),
    path('eliminar_producto/', views.eliminar_producto, name='eliminar_producto'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('editar_producto/', views.editar_producto, name='editar_producto'),
    path('buscar_producto/', views.buscar_producto, name='buscar_producto'),
]