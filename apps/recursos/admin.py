from django.contrib import admin
from django.contrib.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from .models import *


class RecursoResouce(ModelResource):
    class Meta:
        model = Recurso


class RecursoAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = RecursoResouce
    list_display = ('id', 'titulo', 'tipo',)
    search_fields = ['id', 'titulo', ]


class PatrocinadorResouce(ModelResource):
    class Meta:
        model = Patrocinador


class PatrocinadorAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = PatrocinadorResouce
    list_display = ('id', 'nombre', 'descripcion',)
    search_fields = ['id', 'nombre', ]


admin.site.register(Patrocinador, PatrocinadorAdmin)
admin.site.register(Recurso, RecursoAdmin)
