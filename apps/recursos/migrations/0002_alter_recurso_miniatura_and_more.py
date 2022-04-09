# Generated by Django 4.0.3 on 2022-04-09 05:03

from django.db import migrations, models
import educasec.utils.defs
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('recursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurso',
            name='miniatura',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(educasec.utils.defs.update_filename, *(), **{'model_name': 'recurso', 'path_name': '2022/04/09'}), verbose_name='Miniatura'),
        ),
        migrations.AlterField(
            model_name='recurso',
            name='original_filename',
            field=models.FileField(upload_to=functools.partial(educasec.utils.defs.update_filename, *(), **{'model_name': 'recurso', 'path_name': '2022/04/09'}), verbose_name='Archivo Original'),
        ),
        migrations.AlterField(
            model_name='recurso',
            name='tipo',
            field=models.CharField(choices=[('A', 'Audiolibro'), ('H', 'Ficha de Trabajo (Archivo)'), ('F', 'Ficha de Trabajo (Enlace)'), ('G', 'Juego (Archivo)'), ('J', 'Juego (Enlace)'), ('L', 'Libro (Archivo)'), ('B', 'Libro (Enlace)'), ('P', 'Podcast'), ('R', 'Producción Audiovisual'), ('U', 'Producción de Textos (Archivo)'), ('T', 'Producción de Textos (Enlace)'), ('Y', 'Video')], max_length=1, verbose_name='Tipo'),
        ),
    ]