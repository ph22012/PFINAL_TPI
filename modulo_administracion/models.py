from django.db import models

# Create your models here.
class Configuration(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    pathLogo = models.CharField(max_length=100, null=True, blank=True)
    path_slogan = models.CharField(max_length=100, null=True, blank=True)
    color_pallette = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    isPointActive = models.BooleanField(default=False)#programa de lealtad
    configurationPast = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

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


class Role(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=256)

class Employee(models.Model):
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

