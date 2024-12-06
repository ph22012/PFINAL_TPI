from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('catalogo/', views.catalogo_productos, name='catalogo_productos'),
    path('menu/', views.menu_diario, name='menu_diario'),
]