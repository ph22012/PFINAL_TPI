import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_pedidos', '0001_initial'),
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
                ('order_date', models.DateTimeField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('id_address', models.ForeignKey(db_column='id_address', on_delete=django.db.models.deletion.CASCADE, to='gestion_pedidos.customeraddress')),
                ('id_cart', models.ForeignKey(db_column='id_cart', on_delete=django.db.models.deletion.CASCADE, to='gestion_pedidos.shoppingcart')),
            ],
        ),
    ]
