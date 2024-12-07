from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Employee, ShoppingCart, Customer, CustomerAddress,
    Departamento, Distrito, Coupon, Detail, Municipio, Rol,Configuration, RewardPoints
)


admin.site.register(Employee)
admin.site.register(ShoppingCart)
admin.site.register(Customer)
admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Distrito)
admin.site.register(CustomerAddress)
admin.site.register(Coupon)
admin.site.register(Detail)
admin.site.register(Rol)
admin.site.register(Configuration)
admin.site.register(RewardPoints)