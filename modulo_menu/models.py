from django.db import models

# Create your models here.
# category, product, menu
class Category(models.Model):
    id_category = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=256)


class Product(models.Model):
    id_product = models.AutoField(primary_key=True, auto_created=True)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=256) #no esta en el modelo
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    count = models.IntegerField()
    dailyMenuDate = models.DateField()   

#class Menu(models.Model):

"""
id
producto
cantidad
"""    