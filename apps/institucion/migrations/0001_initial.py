# Generated by Django 4.0.3 on 2022-03-14 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('nombres', models.CharField(max_length=150, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(max_length=150, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(max_length=150, verbose_name='Apellido Materno')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Direccion')),
                ('tipo_documento', models.CharField(choices=[('DNI', 'DNI'), ('CEX', 'Carnét de Extranjeria')], default='DNI', max_length=3, verbose_name='Tipo de Documento')),
                ('nro_documento', models.CharField(max_length=12, unique=True, verbose_name='Numero de Documento de Identidad')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Direccion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InstitucionDocente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
