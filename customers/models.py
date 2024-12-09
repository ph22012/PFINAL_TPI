from django.db import models
from django.contrib.auth.models import AbstractUser
from modulo_administracion.models import Role, Customer, RewardPoints
from modulo_catalogo.models import Product
from gestion_pedidos.models import ShoppingCart, Departamento, Distrito, Detail, Municipio

# Create your models here.




#SE CREAN AQUI PARA LA PRUEBA, PERO SE DEBE CREAR EN EL MODULO DE ADMINISTRACION

# class CustomUser(AbstractUser):
#     #Validaciones para saber cual usuario es
#     is_customer = models.BooleanField(default=False)
#     is_employee = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.username
    
# class Customer(models.Model):
#     id_customer = models.AutoField(primary_key=True)
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
#     #PASSWORD SE ESTA HEREDADO DE CUSTOMUSER, ES DECIR QUE AUN SE ENCRIPTA EL PASSWORD
#     firstName = models.CharField(max_length=256)
#     lastName = models.CharField(max_length=256)
#     id_points = models.IntegerField(null=True, blank=True) #Se debe crear una tabla relacionada con puntos
    
#     def __str__(self):
#         return str(self.user)

# class Employee(models.Model):
#     id_employee = models.AutoField(primary_key=True)
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
#     firstName = models.CharField(max_length=256)
#     lastName = models.CharField(max_length=256)
#     is_active = models.BooleanField(default=True)
#     id_rol = models.IntegerField() #luego se agrega una tabla relacionada con roles
    
#     def __str__(self):
#         return str(self.user)