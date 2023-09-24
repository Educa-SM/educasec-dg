from django.contrib import admin
from .models import *
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Nivel
class NivelResouce(resources.ModelResource):
    class Meta:
        model = Nivel
        fields = ('nombre',)


class NivelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre',)
    resources_class = NivelResouce


# Grado
class GradoResouce(resources.ModelResource):
    class Meta:
        model = Grado
        fields = ('nombre', 'nivel')


class GradoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre', 'nivel']
    list_display = ('nombre', 'nivel')
    resources_class = GradoResouce


# curso


class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'codigo_inscripcion',
                    'periodo', 'year', 'estate', 'creation_date')



class AlumnoInscripcionCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'curso','estate' ,'creation_date')


admin.site.register(Nivel, NivelAdmin)
admin.site.register(Grado, GradoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(AlumnoInscripcionCurso, AlumnoInscripcionCursoAdmin)
