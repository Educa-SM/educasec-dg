# Generated by Django 4.0.3 on 2023-03-16 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlumnoInscripcionCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
                ('periodo', models.IntegerField(default=1)),
                ('year', models.IntegerField()),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('codigo_inscripcion', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Codigo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Grado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
                ('nombre', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TipoCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.CharField(default='A', max_length=1)),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipos_cursos', to='cursos.grado')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='grado',
            name='nivel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grados', to='cursos.nivel'),
        ),
    ]
