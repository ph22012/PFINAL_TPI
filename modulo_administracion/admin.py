from django.contrib import admin

# Register your models here.
from .models import Configuration, Role, Employee, Customer

admin.site.register(Configuration)
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Customer)
