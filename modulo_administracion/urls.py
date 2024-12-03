from django.urls import path
from . import views

urlpatterns = [
    path('', views.GeneralView, name='GeneralView'),
    path('configuracion/', views.configuration, name='configuration'),
    
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