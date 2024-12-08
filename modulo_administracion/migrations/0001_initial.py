import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('pathLogo', models.CharField(blank=True, max_length=100, null=True)),
                ('path_slogan', models.CharField(blank=True, max_length=100, null=True)),
                ('color_pallette', models.CharField(blank=True, max_length=100, null=True)),
                ('color_pallette_bg', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('isPointActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('tipo_descuento', models.CharField(choices=[('PORCENTAJE', 'Descuento Porcentual'), ('MONTO_FIJO', 'Descuento Monto Fijo')], max_length=20)),
                ('valor_descuento', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_vencimiento', models.DateTimeField()),
                ('activo', models.BooleanField(default=True)),
                ('uso_maximo', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='RewardPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_date', models.DateTimeField()),
                ('points_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_customer', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id_employee', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=256)),
                ('lastName', models.CharField(max_length=256)),
                ('is_active', models.BooleanField(default=True)),
                ('id_rol', models.ForeignKey(db_column='id_rol', on_delete=django.db.models.deletion.CASCADE, to='modulo_administracion.role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id_customer', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=256)),
                ('lastName', models.CharField(max_length=256)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
                ('id_points', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_administracion.rewardpoints')),
            ],
        ),
    ]
