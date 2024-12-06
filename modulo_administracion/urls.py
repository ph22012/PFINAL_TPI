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
    path('customers/list_customers_partial/', views.list_customers_partial, name='list_customers_partial'),
    path('customers/create/', views.create_customer, name='create_customer'),
    path('customers/create_customer_partial/', views.create_customer_partial, name='create_customer_partial'),
    path('customers/edit/<int:id>/', views.edit_customer, name='edit_customer'),
    path('customers/edit_customer_partial/<int:id>/', views.edit_customer_partial, name='edit_customer_partial'),
    path('customers/delete/<int:id>/', views.delete_customer, name='delete_customer'),
]