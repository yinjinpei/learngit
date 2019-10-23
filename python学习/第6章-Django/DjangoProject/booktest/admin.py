from django.contrib import admin

# Register your models here.

from .models import *


class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id','btitle','bpub_date']


class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['id','hname','hgender','hcontent']


admin.site.register(BookInfo,BookInfoAdmin)
admin.site.register(HeroInfo,HeroInfoAdmin)

