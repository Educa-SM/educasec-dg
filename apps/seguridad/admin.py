from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin 

# Register your models here.


class UserAdmin(UserAdmin, admin.ModelAdmin):
   search_fileds = ['username','first_name', 'last_name','email']
   list_display = ['username','first_name', 'last_name','email']
   fieldsets = (('Usuario', {'fields': ('username', 'password')}),
                ('Informacion Personal', {'fields': ('first_name','last_name','birth_date','email','groups')}),
                ('Permissions', {'fields': ('is_active','is_staff',)}),)

admin.site.register(User,UserAdmin)