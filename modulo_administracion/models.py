from django.db import models

# Create your models here.
class Configuration(models.Model):
    id_configuration = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    path_logo = models.CharField(max_length=100)
    path_slogan = models.CharField(max_length=100)
    color_pallette = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    isPointActive = models.BooleanField(default=False)#programa de lealtad


class Role(models.Model):
    id_role = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

class Employee(models.Model):
    id_employee = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    isActive = models.BooleanField(default=True)
    id_role = models.ForeignKey(Role, on_delete=models.CASCADE)

class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    user = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    #id_points = models.ForeignKey(Reward_Points, on_delete=models.CASCADE)
