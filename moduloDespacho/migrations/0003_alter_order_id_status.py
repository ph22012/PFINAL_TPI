# Generated by Django 5.1.3 on 2024-12-08 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduloDespacho', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id_status',
            field=models.ForeignKey(db_column='id_status', on_delete=django.db.models.deletion.CASCADE, to='moduloDespacho.order_status'),
        ),
    ]
