# Generated by Django 4.0.3 on 2023-03-20 01:53

from django.db import migrations, models
import educasm.utils.defs
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('recursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembroproyecto',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(educasm.utils.defs.update_filename, *(), **{'model_name': 'miembro_proyecto', 'path_name': '2023/03/19'}), verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='patrocinador',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(educasm.utils.defs.update_filename, *(), **{'model_name': 'patrocinador', 'path_name': '2023/03/19'}), verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='recurso',
            name='miniatura',
            field=models.ImageField(upload_to=functools.partial(educasm.utils.defs.update_filename, *(), **{'model_name': 'recurso', 'path_name': '2023/03/19'}), verbose_name='Miniatura'),
        ),
        migrations.AlterField(
            model_name='recurso',
            name='original_filename',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(educasm.utils.defs.update_filename, *(), **{'model_name': 'recurso', 'path_name': '2023/03/19'}), verbose_name='Archivo Original'),
        ),
    ]
