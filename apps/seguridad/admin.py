from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from .models import User


# Register your models here.
class GroupResource(ModelResource):
    class Meta:
        model = Group
        fields = ('id', 'name')


class GroupAdmin(ImportExportModelAdmin, ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name',)
    resources_class = GroupResource


class UserAdmin(UserAdmin, ModelAdmin):
    search_fileds = ['username', 'first_name', 'last_name', 'email']
    list_display = ['username', 'alumno', 'docente']
    fieldsets = (('Usuario', {'fields': ('username', 'password')}),
                 ('Informacion Personal', {
                  'fields': ('first_name', 'last_name', 'email', 'groups')}),
                 ('Permissions', {'fields': ('is_active', 'is_staff',)}),)


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
