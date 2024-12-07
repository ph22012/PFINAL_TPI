from django.contrib import admin
from .models import Customer, Employee, CustomUser
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Employee)