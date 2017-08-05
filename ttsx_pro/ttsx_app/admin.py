from django.contrib import admin
from .models import *
# Register your models here.


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gkucun', 'gtype']
    list_display_links = ('gtitle', 'gtype',)
    list_editable = ('gclick', )
    list_per_page = 15

    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )


admin.site.register(UserInfo)
admin.site.register(TypeInfo)
admin.site.register(GoodsInfo, GoodsAdmin)
