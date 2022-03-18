# Generated by Django 4.0.3 on 2022-03-17 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recursos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institucion', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurso',
            name='creation_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recurso',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucion.institucion'),
        ),
        migrations.AddField(
            model_name='recurso',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_update', to=settings.AUTH_USER_MODEL),
        ),
    ]
