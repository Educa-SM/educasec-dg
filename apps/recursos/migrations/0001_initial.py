# Generated by Django 4.0.3 on 2022-03-18 21:36

from django.db import migrations, models
import django.db.models.deletion
import educasec.utils.defs
import functools


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institucion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Juego',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
                ('texto', models.CharField(blank=True, max_length=255, null=True, verbose_name='Texto')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TipoJuego',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
                ('titulo', models.CharField(default='', max_length=500, verbose_name='Título')),
                ('descripcion', models.CharField(max_length=500, verbose_name='Descripción')),
                ('contenido', models.CharField(max_length=500, verbose_name='Contenido')),
                ('tipo', models.CharField(max_length=1, verbose_name='Tipo')),
                ('original_filename', models.FileField(upload_to=functools.partial(educasec.utils.defs.update_filename, *(), **{'model_name': 'recurso', 'path_name': '2022/03/18'}), verbose_name='Archivo Original')),
                ('miniatura', models.ImageField(blank=True, null=True, upload_to=functools.partial(educasec.utils.defs.update_filename, *(), **{'model_name': 'recurso', 'path_name': '2022/03/18'}), verbose_name='Miniatura')),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucion.institucion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpcionJuego',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
                ('pregunta', models.CharField(blank=True, max_length=255, null=True, verbose_name='Pregunta')),
                ('texto', models.CharField(max_length=255, verbose_name='Texto')),
                ('juego', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recursos.juego')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='juego',
            name='recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recursos.recurso'),
        ),
        migrations.AddField(
            model_name='juego',
            name='tipo_juego',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recursos.tipojuego'),
        ),
    ]
