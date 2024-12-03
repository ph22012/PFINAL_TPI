# Generated by Django 5.1.3 on 2024-12-03 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('path_logo', models.CharField(max_length=100)),
                ('path_slogan', models.CharField(max_length=100)),
                ('color_pallette', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('isPointActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id_customer', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=256)),
                ('lastname', models.CharField(max_length=256)),
                ('user', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id_role', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id_employee', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=256)),
                ('lastname', models.CharField(max_length=256)),
                ('username', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('isActive', models.BooleanField(default=True)),
                ('id_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_administracion.role')),
            ],
        ),
    ]
