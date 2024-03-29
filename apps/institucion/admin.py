from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class DocenteResource (resources.ModelResource):
    class Meta:
        model = Docente
        fields = ('nro_documento', 'nombres', 'apellido_paterno',
                  'apellido_materno', 'tipo_documento', 'user','estate')


class DocenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nro_documento', 'nombres',
                     'apellido_paterno', 'apellido_materno']
    list_display = ('nro_documento', 'tipo_documento', 'nombres',
                    'apellido_paterno', 'apellido_materno', 'user','estate')
    resources_class = DocenteResource


class InstitucionResource(resources.ModelResource):
    class Meta:
        model = Institucion
        fields = ('id', 'nombre', 'direccion',)


class InstitucionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre', 'direccion']
    list_display = ('id', 'nombre', 'direccion',)
    resources_class = InstitucionResource


class AlumnoResource (resources.ModelResource):
    class Meta:
        model = Alumno
        fields = ('nro_documento', 'nombres', 'apellido_paterno',
                  'apellido_materno', 'tipo_documento', 'user')


class AlumnoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nro_documento', 'nombres',
                     'apellido_paterno', 'apellido_materno']
    list_display = ('nro_documento', 'tipo_documento', 'nombres',
                    'apellido_paterno', 'apellido_materno', 'user')
    resources_class = AlumnoResource


class MensajeInicioResource (resources.ModelResource):
    class Meta:
        model = MensajeInicio
        fields = ('titulo', 'fecha_inicio', 'fecha_fin')


class MensajeInicioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['titulo', ]
    list_display = ('titulo', 'fecha_inicio', 'fecha_fin')
    resources_class = MensajeInicioResource


admin.site.register(Docente, DocenteAdmin)
admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(MensajeInicio, MensajeInicioAdmin)
