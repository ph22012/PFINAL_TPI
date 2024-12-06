from django.db import models

# Create your models here.
class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    
    class Meta:
        db_table = "category"
        managed = False
        
    def __str__(self):
        return self.name

class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    id_category = models.ForeignKey('Category',to_field='id_category',db_column='id_category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    count = models.IntegerField()
    daily_menu_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = "product"
        managed = False

    def __str__(self):
        return self.name