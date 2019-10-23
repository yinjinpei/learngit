from django.contrib import admin

# Register your models here.

from .models import *


class HeroInfoInline(admin.TabularInline):
    '''关联对象：
        admin.StackedInline：正常的列表显示方式
        admin.TabularInline：表格显示方式
    '''
    model = HeroInfo
    extra = 3

class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'btitle', 'bpub_date']  # 显示的内容
    list_filter = ['btitle']  # 过滤字段，过滤框会出现在右侧
    search_fields = ['btitle', 'bpub_date']  # 搜索框,根据btitle和bpub_date字段搜索
    list_per_page = 10  # 分页，每页显示的个数

    # 添加、修改页属性: fields和fieldsets二选一
    # fields = ['bpub_date','btitle']    # 属性的先后顺序
    fieldsets = [
        ('书名', {'fields': ['btitle']}),
        ('英雄人物', {'fields': ['bpub_date']}),
    ]  # 属性分组
    inlines = [HeroInfoInline]

class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'hname', 'hgender', 'hcontent']


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
