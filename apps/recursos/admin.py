from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class RecursoResouce(resources.ModelResource):
    class Meta:
        model = Recurso
        fields = ('titulo',)


class RecursoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['titulo']
    list_display = ('titulo',)
    resources_class = RecursoResouce


admin.site.register(Recurso, RecursoAdmin)
