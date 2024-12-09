from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.registro, name='signup'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('principal/', views.principal, name='principal'),
    path('productos/', views.productos, name='productos'),
    path('carrito/', views.carrito, name='carrito'),
    path('logout/', views.logout, name='logout'),
]