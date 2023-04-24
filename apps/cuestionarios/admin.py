from django.contrib import admin
from django.contrib.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from .models import *


# pregunta
class PreguntaResouce(ModelResource):
    class Meta:
        model = Pregunta
        fields = ('cuestionario','texto', 'tipo', 'puntaje_asignado',)


class PreguntaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['texto', 'tipo', 'cuestionario', ]
    list_display = ('id', 'texto','cuestionario',
                    'intentos_disponibles', 'puntaje_asignado',
                    'creation_date')
    resources_class = PreguntaResouce


class OpcionPreguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'texto', 'pregunta', 'correcta')


# cuestionario
class CuestionarioResouce(ModelResource):
    class Meta:
        model = Cuestionario
        fields = ('nombre', 'tipo_curso',)


class CuestionarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre', 'tipo_curso', ]
    list_display = ('id', 'nombre', 'fecha_asignacion',
                    'fecha_expiracion', 'curso',)
    resources_class = CuestionarioResouce


class SolucionResouce(ModelResource):
    class Meta:
        model = Solucion


class SolucionAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = SolucionResouce
    list_display = ('id', 'alumno', 'cuestionario', 'fecha_solucion',
                    'fecha_revision',)
    search_fields = ['id', 'comentario', ]


class SolucionPreguntaResouce(ModelResource):
    class Meta:
        model = SolucionPregunta


class SolucionPreguntaAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = SolucionPreguntaResouce
    list_display = ('id', 'comentario', 'respuesta', 'intentos_tomados', 'puntaje_obtenido',
                    'situacion_respuesta',)
    search_fields = ['id', 'respuesta', 'comentario']


admin.site.register(Pregunta,  PreguntaAdmin)
admin.site.register(OpcionPregunta, OpcionPreguntaAdmin)
admin.site.register(Cuestionario, CuestionarioAdmin)
admin.site.register(Solucion, SolucionAdmin)
admin.site.register(SolucionPregunta, SolucionPreguntaAdmin)
