from django.db import models

# Modelo de Configuración del negocio
class Configuration(models.Model):
    name = models.CharField(max_length=256)
    main_logo = models.CharField(max_length=256)
    slogan = models.CharField(max_length=256)
    color_palette = models.CharField(max_length=256)
    address = models.TextField()
    is_points_active = models.BooleanField(default=False)

# Modelos de localización
class Departamento(models.Model):
    name = models.CharField(max_length=256)

class Municipio(models.Model):
    name = models.CharField(max_length=256)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

class Distrito(models.Model):
    name = models.CharField(max_length=256)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

# Modelo de cliente y dirección
class Customer(models.Model):
    user = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    id_points = models.IntegerField()

class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
    address = models.TextField()

# Modelo de productos y categorías
class Category(models.Model):
    name = models.CharField(max_length=256)

class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    count = models.IntegerField()
    daily_menu_date = models.DateField(null=True, blank=True)

class ShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Detail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shoppingcart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    amount = models.IntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

# Modelo de Cupones y Puntos
class RewardPoints(models.Model):
    exp_date = models.DateTimeField()
    points_count = models.IntegerField()

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=256)
    coupon_discount = models.DecimalField(max_digits=4, decimal_places=2)
    exp_date = models.DateTimeField()

# Modelo de pedidos

# Roles de empleados
class Rol(models.Model):
    name = models.CharField(max_length=256)

class Employee(models.Model):
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)

#Se desactivan momentaneamente las tablas relacionadas con pedidos
"""class OrderStatus(models.Model):
    status = models.CharField(max_length=256)

class Order(models.Model):
    shoppingcart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)"""