# Generated by Django 5.1.3 on 2024-12-04 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_administracion', '0003_alter_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]