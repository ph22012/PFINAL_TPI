from django.db import models

# Create your models here.
class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    path_logo = models.CharField(max_length=100)
    path_slogan = models.CharField(max_length=100)
    color_pallette = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    isPointActive = models.BooleanField(default=False)#programa de lealtad
    idconfigurationPast = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    isActive = models.BooleanField(default=True)
    id_role = models.ForeignKey(Role, on_delete=models.CASCADE)

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    user = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    idConfiguration = models.ForeignKey(Configuration, on_delete=models.CASCADE, null=True, blank=True)
    #id_points = models.ForeignKey(Reward_Points, on_delete=models.CASCADE)
