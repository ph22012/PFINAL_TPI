# Generated by Django 5.1.3 on 2024-12-05 03:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order_status',
            fields=[
                ('id_status', models.IntegerField(primary_key=True, serialize=False)),
                ('status', models.TextField()),
            ],
            options={
                'db_table': 'order_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id_order', models.AutoField(primary_key=True, serialize=False)),
                ('id_cart', models.IntegerField()),
                ('id_address', models.IntegerField()),
                ('id_cupon', models.IntegerField()),
                ('id_employee', models.IntegerField()),
                ('order_date', models.DateTimeField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('id_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moduloDespacho.order_status')),
            ],
        ),
    ]
