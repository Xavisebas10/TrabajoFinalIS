# Generated by Django 5.1.4 on 2025-07-06 04:26

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
            name='DispositivoIoT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('peligro', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Activador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('accion', models.CharField(max_length=100)),
                ('dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activadores', to='IS.dispositivoiot')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_medicion', models.CharField(choices=[('CO2', 'CO₂'), ('PM25', 'Partículas PM2.5'), ('TEMP', 'Temperatura'), ('HUMEDAD', 'Humedad')], max_length=20)),
                ('unidad', models.CharField(max_length=20)),
                ('umbral_min', models.FloatField()),
                ('umbral_max', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
                ('dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensores', to='IS.dispositivoiot')),
            ],
        ),
        migrations.CreateModel(
            name='Medicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mediciones', to='IS.sensor')),
            ],
        ),
        migrations.AddField(
            model_name='dispositivoiot',
            name='zona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dispositivos', to='IS.zona'),
        ),
        migrations.CreateModel(
            name='Usuario',
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
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('rol', models.CharField(choices=[('ADMIN', 'Administrador'), ('SUPERVISOR', 'Supervisor de Planta'), ('TECNICO', 'Técnico de Mantenimiento'), ('ANALISTA', 'Analista de Datos')], max_length=20)),
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
            name='ProtocoloEmergencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('activadores', models.ManyToManyField(to='IS.activador')),
                ('sensores', models.ManyToManyField(to='IS.sensor')),
                ('zona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IS.zona')),
                ('creado_por', models.ForeignKey(limit_choices_to={'rol': 'SUPERVISOR'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mantenimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(choices=[('PREVENTIVO', 'Preventivo'), ('CORRECTIVO', 'Correctivo')], max_length=20)),
                ('descripcion', models.TextField()),
                ('duracion_horas', models.FloatField()),
                ('dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IS.dispositivoiot')),
                ('tecnico', models.ForeignKey(limit_choices_to={'rol': 'TECNICO'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogAuditoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(max_length=255)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
