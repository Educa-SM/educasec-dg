from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class GroupResource(resources.ModelResource):
   class Meta:
      model = Group
      fields = ('id','name')

class GroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   search_fields = ['name']
   list_display =('id','name',)
   resources_class = GroupResource

class UserAdmin(UserAdmin, admin.ModelAdmin):
   search_fileds = ['username','first_name', 'last_name','email']
   list_display = ['username']
   fieldsets = (('Usuario', {'fields': ('username', 'password')}),
                ('Informacion Personal', {'fields': ('first_name','last_name','birth_date','email','groups')}),
                ('Permissions', {'fields': ('is_active','is_staff',)}),)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

admin.site.register(User,UserAdmin)
