from django.urls import path
from . import views
urlpatterns = [
    path('', views.GeneralView, name='GeneralView'),
    path('configuracion/', views.configuration, name='configuration'),
    path('roles/', views.roles, name='roles'),
    path('empleados/', views.employees, name='employees'),
    path('custumers/', views.customers, name='customers'),
]