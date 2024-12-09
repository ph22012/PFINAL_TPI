from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.registro, name='signup'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('principal/', views.principal, name='principal'),
<<<<<<< HEAD
    path('logout/', views.custom_logout, name='logout'),
=======
    path('productos/', views.productos, name='productos'),
    path('carrito/', views.carrito, name='carrito'),
    path('logout/', views.logout, name='logout'),
>>>>>>> 4165b2048be9b1870e0e1e3ca6611d8f419a2017
]