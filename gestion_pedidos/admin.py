from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    ShoppingCart, 
    Departamento, Distrito,  Detail, Municipio
)


admin.site.register(ShoppingCart)
admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Distrito)
admin.site.register(Detail)
