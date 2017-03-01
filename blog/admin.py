from django.contrib import admin
from blog.models import *

# Register your models here.
#2017-3-1



class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','author','created',)

admin.site.register(Catagory, CatagoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
