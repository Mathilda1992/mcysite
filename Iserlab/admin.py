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
    list_display = ('id','exp_name','exp_owner_name','is_shared','exp_image_count','exp_createtime','exp_updatetime',)
    filter_horizontal = ('exp_images','exp_network',)

    #ERRORS:
    # <class 'Iserlab.admin.ExperimentAdmin'>: (admin.E109) The value of 'list_display[3]' must not be a ManyToManyField.
    # <class 'Iserlab.admin.ExperimentAdmin'>: (admin.E109) The value of 'list_display[4]' must not be a ManyToManyField.


class VMImageAdmin(admin.ModelAdmin):
    list_display = ('id','image_id','name','owner_name','own_project','is_public','is_shared')
    filter_horizontal = ('tags',)


class NetworkAdmin(admin.ModelAdmin):
    list_display = ('id','network_name','subnet_name','cidr','owner_name','is_shared','created_at',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name','createtime')

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id','name','desc','exp','teacher','group','delivery_time','update_time',)
    search_fields = ('teacher','group','exp',)
    list_filter = ('teacher','group','exp',)

class SocreAdmin(admin.ModelAdmin):
    list_display = ('id','exp','stu','createTime','situation','finishedTime','score','scoreTime')

class VMAdmin(admin.ModelAdmin):
    list_display = ('id','owner_name','exp','image','network','created_at')

class ExpInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','owner_name','exp','createtime','instance_status')

class VMInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','name','owner_name','server_id','belong_exp_instance_id','vm','ip',)

class NetworkInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','name','owner_name','network_instance_id','belong_exp_instance_id','network')

class RouterInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','name','createtime','owner_username','gateway_ip_address','routerIntance_id')

class PortInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','owner_username','status','device_owner','network_id','ip_address','portInstance_id')

class ImageCartAdmin(admin.ModelAdmin):
    list_display = ('id','user','image','createtime')

class NetworkCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'network', 'createtime')

class MyTempExpAdmin(admin.ModelAdmin):
    list_display = ('id','teacher','exp','createtime')

class MyTempGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher','group', 'createtime')

class MyTempImageAdmin(admin.ModelAdmin):
    list_display = ('id','teacher','image','createtime')

class MyTempNetworkAdmin(admin.ModelAdmin):
    list_display = ('id','teacher','network','createtime')

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
admin.site.register(ImageCart,ImageCartAdmin)
admin.site.register(NetworkCart,NetworkCartAdmin)
admin.site.register(NetworkInstance,NetworkInstanceAdmin)
admin.site.register(RouterInstance,RouterInstanceAdmin)
admin.site.register(PortInstance,PortInstanceAdmin)
admin.site.register(ExpInstance,ExpInstanceAdmin)

# admin.site.register(TempExp,TempExpAdmin)
# admin.site.register(TempGroup,TempGroupAdmin)

admin.site.register(MyTempExp,MyTempExpAdmin)
admin.site.register(MyTempGroup,MyTempGroupAdmin)
admin.site.register(MyTempImage,MyTempImageAdmin)
admin.site.register(MyTempNetwork,MyTempNetworkAdmin)

