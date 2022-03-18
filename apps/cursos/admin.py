from django.contrib import admin
from .models import *
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin
"""
# Nivel
class NivelResouce(resources.ModelResource):
   class Meta:
      model = Nivel
      fields = ('nombre',)

class NivelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['nombre']
   list_display =('nombre',)
   resources_class = NivelResouce

# curso
class CursoResouce(resources.ModelResource):
   class Meta:
      model = Curso
      fields = ('nombre','nivel','institucion')

class CursoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['nombre','nivel','institucion']
   list_display =('nombre','nivel','institucion')
   resources_class = CursoResouce

# cuestionario
class CuestionarioResouce(resources.ModelResource):
   class Meta:
      model = Cuestionario
      fields = ('nombre','docente','curso','fecha_disponible','fecha_expiracion')

class CuestionarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['nombre','docente','curso','fecha_disponible','fecha_expiracion']
   list_display =('nombre','docente','curso','fecha_disponible','fecha_expiracion')
   resources_class = CuestionarioResouce

# pregunta
class PreguntaResouce(resources.ModelResource):
   class Meta:
      model = Pregunta
      fields = ('texto','tipo','docente','curso','institucion')

class PreguntaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['texto','tipo','docente','curso','institucion']
   list_display =('texto','tipo','docente','curso','institucion')
   resources_class = PreguntaResouce


admin.site.register(Nivel, NivelAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Cuestionario, CuestionarioAdmin)"""