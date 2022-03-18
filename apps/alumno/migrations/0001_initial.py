# Generated by Django 4.0.3 on 2022-03-18 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('nro_documento', models.CharField(max_length=12, unique=True, verbose_name='Numero de Documento de Identidad')),
                ('nombres', models.CharField(max_length=150, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(max_length=150, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(max_length=150, verbose_name='Apellido Materno')),
                ('tipo_documento', models.CharField(choices=[('DNI', 'DNI'), ('CEX', 'Carnét de Extranjeria')], default='DNI', max_length=3, verbose_name='Tipo de Documento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlumnoCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('periodo', models.IntegerField(default=1)),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolucionCuestionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('fecha_solucion', models.DateTimeField(verbose_name='Fecha de Solucion')),
                ('fecha_revision', models.DateTimeField(verbose_name='Apellido Paterno')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolucionPregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('respuesta', models.CharField(max_length=250, verbose_name='Respuesta')),
                ('puntaje', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Puntaje Obtenido')),
                ('intentos', models.IntegerField(default=0, verbose_name='Intentos')),
                ('intentos_posibles', models.IntegerField(default=0, verbose_name='Cantidad de Intentos')),
                ('puntaje_pregunta', models.DecimalField(decimal_places=2, default=0, max_digits=14, verbose_name='Puntaje de la Pregunta')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
