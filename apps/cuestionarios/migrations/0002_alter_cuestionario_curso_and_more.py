# Generated by Django 4.0.3 on 2023-03-26 22:15

from django.db import migrations, models
import django.db.models.deletion
import educasm.utils.defs
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_alter_curso_tipo_curso'),
        ('cuestionarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuestionario',
            name='curso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cuestionarios', to='cursos.curso'),
        ),
        migrations.AlterField(
            model_name='cuestionario',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripcion'),
        ),
        migrations.AlterField(
            model_name='cuestionario',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(educasm.utils.defs.update_filename, *(), **{'model_name': 'cuestionario_banco', 'path_name': '2023/03/26'}), verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(educasm.utils.defs.update_filename, *(), **{'model_name': 'pregunta', 'path_name': '2023/03/26'}), verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='texto',
            field=models.CharField(max_length=500, verbose_name='Detalle'),
        ),
    ]
