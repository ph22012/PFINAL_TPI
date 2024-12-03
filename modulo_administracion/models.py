from django.db import models

# Create your models here.
class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    path_logo = models.CharField(max_length=100)
    path_slogan = models.CharField(max_length=100)
    color_pallette = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    isPointActive = models.BooleanField(default=False)

