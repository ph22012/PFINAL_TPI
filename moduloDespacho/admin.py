from django.contrib import admin
from .models import Order, Order_status

# Register your models here.
admin.site.register(Order)
admin.site.register(Order_status)