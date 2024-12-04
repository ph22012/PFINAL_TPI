from django.db import models

# Create your models here.
class Order_status(models.Model):
    id_status = models.IntegerField(primary_key=True)
    status = models.TextField()
    
    #Se indica que ya existe la tabla en la base de datos
    class Meta:
        db_table = 'order_status'
        managed = False
    
    def __str__(self):
        return self.status

class Order(models.Model):
    id_order=models.AutoField(primary_key=True)
    id_cart=models.IntegerField() #esta es FK pero no se ha creado el modelo
    id_address=models.IntegerField() #esta es FK pero no se ha creado el modelo
    id_cupon=models.IntegerField() #esta es FK pero no se ha creado el modelo
    id_employee=models.IntegerField() #esta es FK pero no se ha creado el modelo
    id_status=models.ForeignKey(Order_status,to_field='id_status', on_delete=models.CASCADE) #esta es FK pero no se ha creado el modelo
    order_date=models.DateTimeField()
    last_update = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return str(self.id_order)
