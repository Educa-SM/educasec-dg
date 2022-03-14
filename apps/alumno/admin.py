from django.contrib import admin
from .models import *
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class AlumnoResouce(resources.ModelResource):
   class Meta:
      model = Alumno
      fields = ('nro_documento','nombres','apellido_paterno','apellido_materno','tipo_documento','user')

class AlumnoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['nro_documento','nombres','apellido_paterno','apellido_materno']
   list_display =('nro_documento','tipo_documento','nombres','apellido_paterno','apellido_materno','user')
   resources_class = AlumnoResouce

admin.site.register(Alumno, AlumnoAdmin)