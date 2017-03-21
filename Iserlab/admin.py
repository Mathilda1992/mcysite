# Register your models here.

from django.contrib import admin
from Iserlab.models import *





#this class describe what fields showed on admin UI

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','email',)
#
#
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'stu_username', 'stu_password', 'stu_email',)



class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','name','teacher','stuCount','created_at',)
    filter_horizontal = ('student',)

#
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('id','exp_name','exp_owner','is_shared','exp_image_count','exp_createtime','exp_updatetime',)
    filter_horizontal = ('exp_images','exp_network',)

    #ERRORS:
    # <class 'Iserlab.admin.ExperimentAdmin'>: (admin.E109) The value of 'list_display[3]' must not be a ManyToManyField.
    # <class 'Iserlab.admin.ExperimentAdmin'>: (admin.E109) The value of 'list_display[4]' must not be a ManyToManyField.


class VMImageAdmin(admin.ModelAdmin):
    list_display = ('id','image_id','name','owner','own_project','is_public',)
    filter_horizontal = ('tags',)


class NetworkAdmin(admin.ModelAdmin):
    list_display = ('id','network_name','subnet_name','cidr','owner','is_shared','created_at',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name','createtime')

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id','name','desc','exp','teacher','group','delivery_time','update_time',)
    search_fields = ('teacher','group','exp',)
    list_filter = ('teacher','group','exp',)

class SocreAdmin(admin.ModelAdmin):
    list_display = ('id','exp','stu','createTime','situation','finishedTime','score','scoreTime')

class VMAdmin(admin.ModelAdmin):
    list_display = ('id','owner','exp','image','network','created_at')


class VMInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','name','owner_name','server_id','exp_instance','vm','ip',)

class NetworkInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','name','owner_name','network_instance_id','exp_instance','network')

class RouterInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','name','createtime','owner_username','routerIntance_id')

class PortInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','owner_username','status','device_owner','network_id','ip_address','portInstance_id')
#

admin.site.register(User,UserAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Group,GroupAdmin)
admin.site.register(VMImage,VMImageAdmin)
admin.site.register(Network,NetworkAdmin)
admin.site.register(Experiment,ExperimentAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(VMInstance,VMInstanceAdmin)
admin.site.register(VM,VMAdmin)
admin.site.register(Delivery,DeliveryAdmin)
admin.site.register(Score,SocreAdmin)
admin.site.register(ImageCart)
admin.site.register(NetworkCart)
admin.site.register(NetworkInstance,NetworkInstanceAdmin)
admin.site.register(RouterInstance,RouterInstanceAdmin)
admin.site.register(PortInstance,PortInstanceAdmin)

admin.site.register(TempExp)
admin.site.register(TempGroup)
