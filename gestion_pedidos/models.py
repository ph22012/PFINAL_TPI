from django.db import models
from modulo_catalogo.models import Product

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
    id_departamento = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    
    class Meta:
        db_table = "departamento"
        managed = False
    
    def __str__(self):
        return self.name

class Municipio(models.Model):
    id_municipio = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    id_departamento = models.ForeignKey(Departamento,to_field='id_departamento',db_column='id_departamento', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "municipio"
        managed = False
    def __str__(self):
        return self.name
class Distrito(models.Model):
    id_distrito = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    id_municipio = models.ForeignKey(Municipio, to_field='id_municipio',db_column='id_municipio', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "distrito"
        managed = False
    def __str__(self):
        return self.name

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
""" SE COMENTAN PORQUE NO SE USAN MAS
class Category(models.Model):
    name = models.CharField(max_length=256)

class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    count = models.IntegerField()
    daily_menu_date = models.DateField(null=True, blank=True)"""

class ShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Detail(models.Model):
    product = models.ForeignKey(Product,to_field='id_product',db_column='id_product', on_delete=models.CASCADE)
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