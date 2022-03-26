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
   list_display =('nombre',)
   resources_class = NivelResouce

# Grado
class GradoResouce(resources.ModelResource):
   class Meta:
      model = Grado
      fields = ('nombre','nivel')

class GradoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['nombre','nivel']
   list_display =('nombre','nivel')
   resources_class = GradoResouce

# curso
class CursoResouce(resources.ModelResource):
   class Meta:
      model = Curso
      fields = ('nombre','grado')

class CursoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['nombre','grado']
   list_display =('nombre','grado')
   resources_class = CursoResouce

# cuestionario
class CuestionarioResouce(resources.ModelResource):
   class Meta:
      model = Cuestionario
      fields = ('nombre','curso',)

class CuestionarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['nombre','curso',]
   list_display =('nombre','curso',)
   resources_class = CuestionarioResouce

# pregunta
class PreguntaResouce(resources.ModelResource):
   class Meta:
      model = Pregunta
      fields = ('texto','tipo','curso',)

class PreguntaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['texto','tipo','curso',]
   list_display =('texto','tipo','curso',)
   resources_class = PreguntaResouce

class PreguntaOpcionAdmin(admin.ModelAdmin):
   list_display = ('id', 'texto','pregunta','correcta')


class CursoDocenteAdmin(admin.ModelAdmin):
   list_display = ('id', 'nombre','codigo_inscripcion','periodo','year','estate','creation_date')


admin.site.register(Nivel, NivelAdmin)
admin.site.register(Grado, GradoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Pregunta,  PreguntaAdmin)
admin.site.register(PreguntaOpcion, PreguntaOpcionAdmin)
admin.site.register(Cuestionario, CuestionarioAdmin)
admin.site.register(CursoDocente, CursoDocenteAdmin)
