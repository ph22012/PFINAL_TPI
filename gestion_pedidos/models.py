from django.db import models

# Modelo: Category
class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

# Modelo: Product
class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    count = models.IntegerField()
    dailyMenuDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

# Modelo: Detail
class Detail(models.Model):
    id_detail = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="details")
    amount = models.IntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail {self.id_detail} - Product {self.id_product.name}"

# Modelo: RewardPoints
class RewardPoints(models.Model):
    id_points = models.AutoField(primary_key=True)
    exp_date = models.DateTimeField()
    points_count = models.IntegerField()

    def __str__(self):
        return f"Points {self.points_count}"

# Modelo: Customer
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    firstname = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    id_points = models.ForeignKey(RewardPoints, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastName}"

# Modelo: CustomerAddresses
class CustomerAddresses(models.Model):
    id_address = models.AutoField(primary_key=True)
    address = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")

    def __str__(self):
        return f"{self.address} for {self.customer}"

# Modelo: Cupon
class Cupon(models.Model):
    id_cupon = models.AutoField(primary_key=True)
    cupon_code = models.CharField(max_length=256)
    cupon_disount = models.DecimalField(max_digits=5, decimal_places=2)
    exp_date = models.DateTimeField()

    def __str__(self):
        return self.cupon_code

# Modelo: ShoppingCart
class ShoppingCart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="shopping_carts")

    def __str__(self):
        return f"Cart {self.id_cart} for {self.customer}"

# Modelo: OrderStatus
class OrderStatus(models.Model):
    id_status = models.AutoField(primary_key=True)
    status = models.CharField(max_length=256)

    def __str__(self):
        return self.status

# Modelo: Order
class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    id_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name="orders")
    id_address = models.ForeignKey(CustomerAddresses, on_delete=models.CASCADE, related_name="orders")
    id_cupon = models.ForeignKey(Cupon, on_delete=models.SET_NULL, null=True, blank=True)
    id_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="orders")
    id_employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField()

    def __str__(self):
        return f"Order {self.id_order}"

# Modelo: Employee
class Employee(models.Model):
    id_employee = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    username = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    isActive = models.BooleanField(default=True)
    id_rol = models.ForeignKey("Rol", on_delete=models.CASCADE, related_name="employees")

    def __str__(self):
        return f"{self.firstname} {self.lastName}"

# Modelo: Rol
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

# Modelo: Municipio
class Municipio(models.Model):
    id_municipio = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

# Modelo: Distrito
class Distrito(models.Model):
    id_distrito = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    id_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name="distritos")

    def __str__(self):
        return self.name

# Modelo: Departamento
class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

# Modelo: Configuration
class Configuration(models.Model):
    id_configuration = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    slogan = models.CharField(max_length=256)
    color_pallete = models.CharField(max_length=256)
    address = models.TextField()
    isPointsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

