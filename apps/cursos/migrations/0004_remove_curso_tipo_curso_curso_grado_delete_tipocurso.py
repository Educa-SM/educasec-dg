# Generated by Django 4.1 on 2023-05-09 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_alter_curso_tipo_curso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='tipo_curso',
        ),
        migrations.AddField(
            model_name='curso',
            name='grado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cursos.grado'),
        ),
        migrations.DeleteModel(
            name='TipoCurso',
        ),
    ]