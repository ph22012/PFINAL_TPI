from django.db import models

# Create your models here.
class Order_status(models.Model):
    id_status = models.IntegerField(primary_key=True)
    status = models.TextField()

class Order(models.Model):
    id_order=models.IntegerField(primary_key=True)
    id_cart=models.IntegerField() #esta es FK pero no se ha creado el modelo
    id_address=models.IntegerField() #esta es FK pero no se ha creado el modelo
    id_cupon=models.IntegerField() #esta es FK pero no se ha creado el modelo
    id_employee=models.IntegerField() #esta es FK pero no se ha creado el modelo
    id_status=models.ForeignKey(Order_status, on_delete=models.CASCADE) #esta es FK pero no se ha creado el modelo
    id_status=models.IntegerField() #esta es FK pero no se ha creado el modelo
    order_date=models.DateTimeField() 
