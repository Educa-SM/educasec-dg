from django.contrib import admin
from django.contrib.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from .models import *


class CuestionarioCursoResouce(ModelResource):
    class Meta:
        model = CuestionarioCurso


class CuestionarioCursoAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = CuestionarioCursoResouce
    list_display = ('id', 'nombre', 'cuestionario',)
    search_fields = ['id', 'nombre', ]


class SolucionCuestionarioResouce(ModelResource):
    class Meta:
        model = SolucionCuestionario


class SolucionCuestionarioAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = SolucionCuestionarioResouce
    list_display = ('id', 'comentario', 'cuestionario_curso',)
    search_fields = ['id', 'comentario', ]


class SolucionPreguntaResouce(ModelResource):
    class Meta:
        model = SolucionPregunta


class SolucionPreguntaAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = SolucionPreguntaResouce
    list_display = ('id', 'respuesta', 'intentos_tomados',)
    search_fields = ['id', 'respuesta', ]


admin.site.register(CuestionarioCurso, CuestionarioCursoAdmin)
admin.site.register(SolucionCuestionario, SolucionCuestionarioAdmin)
admin.site.register(SolucionPregunta, SolucionPreguntaAdmin)
