from django.urls import path
from . import views

urlpatterns = [
    path('', views.GeneralView, name='GeneralView'),
    path('configuracion/', views.configuration_home, name='configuration_home'),
    path('gestionar-configuraciones/', views.gestionar_configuraciones, name='gestionar_configuraciones'),
    path('gestionar-configuraciones-view/', views.gestionar_configuraciones_view, name='gestionar_configuraciones_view'),
    path('editar-configuracion/<int:configuracion_id>/', views.editar_configuracion, name='editar_configuracion'),
    path('eliminar-configuracion/<int:configuracion_id>/', views.eliminar_configuracion, name='eliminar_configuracion'),

   #cupones 
    path('gestionar-cupones/', views.gestionar_cupones, name='gestionar_cupones'),
    path('gestionar-cupones-view/', views.gestionar_cupones_view, name='gestionar_cupones_view'),
    path('desactivar-cupon/<int:cupon_id>/<int:flag>/', views.desactivar_cupon, name='desactivar_cupon'),
    path('eliminar-cupon/<int:cupon_id>/', views.eliminar_cupon, name='eliminar_cupon'),
    
    # Roles CRUD
    path('roles/', views.roles, name='roles'),
    path('roles/list/', views.list_roles, name='list_roles'),
    path('roles/create/', views.create_role, name='create_role'),
    path('roles/edit/<int:id>/', views.edit_role, name='edit_role'),
    path('roles/delete/<int:id>/', views.delete_role, name='delete_role'),

    # Employees CRUD
    path('employees/', views.employees, name='employees'),
    path('employees/list/', views.list_employees, name='list_employees'),
    path('employees/create/', views.create_employee, name='create_employee'),
    path('employees/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),

    # Customers CRUD
    path('customers/', views.customers, name='customers'),
    path('customers/list/', views.list_customers, name='list_customers'),
    path('customers/create/', views.create_customer, name='create_customer'),
    path('customers/edit/<int:id>/', views.edit_customer, name='edit_customer'),
    path('customers/delete/<int:id>/', views.delete_customer, name='delete_customer'),
]