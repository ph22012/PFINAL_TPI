import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_pedidos', '0001_initial'),
        ('modulo_administracion', '0001_initial'),
        ('modulo_catalogo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeraddress',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_administracion.customer'),
        ),
        migrations.AddField(
            model_name='detail',
            name='product',
            field=models.ForeignKey(db_column='id_product', on_delete=django.db.models.deletion.CASCADE, to='modulo_catalogo.product'),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_administracion.customer'),
        ),
        migrations.AddField(
            model_name='detail',
            name='shoppingcart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_pedidos.shoppingcart'),
        ),
    ]
