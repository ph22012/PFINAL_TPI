import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('moduloDespacho', '0001_initial'),
        ('modulo_administracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='id_cupon',
            field=models.ForeignKey(blank=True, db_column='id_cupon', null=True, on_delete=django.db.models.deletion.CASCADE, to='modulo_administracion.cupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='id_employee',
            field=models.ForeignKey(db_column='id_employee', on_delete=django.db.models.deletion.CASCADE, to='modulo_administracion.employee'),
        ),
        migrations.AddField(
            model_name='order',
            name='id_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moduloDespacho.order_status'),
        ),
    ]