from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Configuration(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    pathLogo = models.CharField(max_length=100, null=True, blank=True)
    path_slogan = models.CharField(max_length=100, null=True, blank=True)
    color_pallette = models.CharField(max_length=100, null=True, blank=True)
    color_pallette_bg = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    isPointActive = models.BooleanField(default=False)#programa de lealtad


class Cupon(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)
    tipo_descuento = models.CharField(max_length=20, choices=[
        ('PORCENTAJE', 'Descuento Porcentual'),
        ('MONTO_FIJO', 'Descuento Monto Fijo')
    ])
    valor_descuento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField()
    activo = models.BooleanField(default=True)
    uso_maximo = models.IntegerField(default=1)

class RewardPoints(models.Model):
    exp_date = models.DateTimeField()
    points_count = models.IntegerField()

class Role(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=256)

class CustomUser(AbstractUser):
    #Validaciones para saber cual usuario es
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    #PASSWORD SE ESTA HEREDADO DE CUSTOMUSER, ES DECIR QUE AUN SE ENCRIPTA EL PASSWORD
    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    id_points = models.ForeignKey(RewardPoints, on_delete=models.CASCADE) #Se debe crear una tabla relacionada con puntos
    
    def __str__(self):
        return str(self.user)

class Employee(models.Model):
    id_employee = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    id_rol = models.ForeignKey(Role,to_field='id',db_column="id_rol" ,on_delete=models.CASCADE) #luego se agrega una tabla relacionada con roles
    
    def __str__(self):
        return str(self.user)

"""class Employee(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    isActive = models.BooleanField(default=False)
    id_role = models.ForeignKey(Role, on_delete=models.CASCADE)

class Customer(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    user = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}" 
"""
