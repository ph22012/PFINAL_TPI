from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('catalogo/', views.catalogo_productos, name='catalogo_productos'),
    path('menu/', views.menu_diario, name='menu_diario'),
    path('eliminar_producto/', views.eliminar_producto, name='eliminar_producto'),
     # otras rutas
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
]