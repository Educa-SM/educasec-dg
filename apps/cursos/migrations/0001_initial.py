# Generated by Django 4.0.3 on 2022-03-12 01:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alumno', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institucion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuestionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('fecha_disponible', models.DateTimeField(auto_now_add=True)),
                ('fecha_expiracion', models.DateTimeField(auto_now_add=True)),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('creation_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('creation_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('institucion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucion.institucion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('texto', models.CharField(max_length=150, verbose_name='Texto')),
                ('tipo', models.CharField(choices=[('O', 'Domiciliado'), ('R', 'Respuesta Simple')], default='R', max_length=1, verbose_name='Tipo de Pregunta')),
                ('creation_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('curso_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
                ('docente_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucion.docente')),
                ('institucion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucion.institucion')),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_update', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PreguntaOpcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('texto', models.CharField(max_length=250)),
                ('correcta', models.CharField(choices=[('C', 'Correcta'), ('I', 'Incorrecta')], default='I', max_length=1, verbose_name='¿Es correcta?')),
                ('creation_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('pregunta_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.pregunta')),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_update', to=settings.AUTH_USER_MODEL)),
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
                ('estate', models.BooleanField(default=True)),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('creation_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_update', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='curso',
            name='nivel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.nivel'),
        ),
        migrations.AddField(
            model_name='curso',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_update', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CuestionarioPregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('estate', models.BooleanField(default=True)),
                ('reintentos', models.IntegerField(default=1)),
                ('puntaje', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('creation_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('cuestionario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.cuestionario')),
                ('pregunta_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.pregunta')),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_update', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cuestionario',
            name='curso_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso'),
        ),
        migrations.AddField(
            model_name='cuestionario',
            name='docente_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucion.docente'),
        ),
        migrations.AddField(
            model_name='cuestionario',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_update', to=settings.AUTH_USER_MODEL),
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
                ('alumno_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumno.alumno')),
                ('creation_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('curso_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
                ('docente_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucion.docente')),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_update', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
