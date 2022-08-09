from django.contrib import admin
from django.contrib.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from .models import *


# pregunta
class PreguntaBancoResouce(ModelResource):
    class Meta:
        model = PreguntaBanco
        fields = ('texto', 'tipo', 'tipo_curso',)


class PreguntaBancoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['texto', 'tipo', 'tipo_curso', ]
    list_display = ('texto', 'tipo', 'tipo_curso',)
    resources_class = PreguntaBancoResouce


class PreguntaOpcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'texto', 'pregunta_banco', 'correcta')


# cuestionario
class CuestionarioBancoResouce(ModelResource):
    class Meta:
        model = CuestionarioBanco
        fields = ('nombre', 'tipo_curso',)


class CuestionarioBancoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre', 'tipo_curso', ]
    list_display = ('nombre', 'tipo_curso',)
    resources_class = CuestionarioBancoResouce


class CuestionarioResouce(ModelResource):
    class Meta:
        model = Cuestionario


class CuestionarioAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = CuestionarioResouce
    list_display = ('id', 'nombre', 'fecha_asignacion',
                    'fecha_expiracion', 'cuestionario_banco', 'curso',)
    search_fields = ['id', 'nombre', ]


class CuestionarioPreguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pregunta_banco', 'cuestionario',
                    'intentos_disponibles', 'puntaje_asignado',
                    'creation_date')


class SolucionResouce(ModelResource):
    class Meta:
        model = Solucion


class SolucionAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = SolucionResouce
    list_display = ('id', 'alumno', 'cuestionario', 'fecha_solucion',
                    'fecha_revision', 'fecha_solucion')
    search_fields = ['id', 'comentario', ]


class SolucionPreguntaResouce(ModelResource):
    class Meta:
        model = SolucionPregunta


class SolucionPreguntaAdmin(ImportExportModelAdmin, ModelAdmin):
    resources_class = SolucionPreguntaResouce
    list_display = ('id', 'respuesta', 'intentos_tomados', 'comentario',)
    search_fields = ['id', 'respuesta', 'comentario']


admin.site.register(PreguntaBanco,  PreguntaBancoAdmin)
admin.site.register(PreguntaOpcion, PreguntaOpcionAdmin)
admin.site.register(Cuestionario, CuestionarioAdmin)
admin.site.register(Solucion, SolucionAdmin)
admin.site.register(SolucionPregunta, SolucionPreguntaAdmin)
admin.site.register(CuestionarioBanco, CuestionarioBancoAdmin)
admin.site.register(CuestionarioPregunta, CuestionarioPreguntaAdmin)
