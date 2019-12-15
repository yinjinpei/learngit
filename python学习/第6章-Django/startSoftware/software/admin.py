from django.contrib import admin

# Register your models here.

from .models import *

class AppAdmin(admin.ModelAdmin):
    list_display = ['id', 'remark','appName', 'appDir']
    fieldsets = [
        ('base',{'fields':['remark','appName']}),
        ('super',{'fields':['appDir']})
    ]

admin.site.register(AppInfo,AppAdmin)

