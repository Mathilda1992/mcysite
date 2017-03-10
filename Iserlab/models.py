from __future__ import unicode_literals

from django.db import models


#******define your own fields here**********

#if we want to reduce the length of context, compress when save it into db, decompress it when read it from db,we should define a CompressedTextField
class CompressedTextField(models.TextField):
    """
    model Fields for storing text in a compressed format (bz2 by default)
    """
    def from_db_value(self, value, expression, connection, context):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value

    def to_python(self, value):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value

    def get_prep_value(self, value):
        if not value:
            return value
        try:
            value.decode('base64')
            return value
        except Exception:
            try:
                return value.encode('utf-8').encode('bz2').encode('base64')
            except Exception:
                return value



#if we want to save a list into table, and we can read it by List format,we should define a ListField
import ast

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)  # use str(value) in Python 3

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)



# ************************Create your models here.*****************************8
class User(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    # role = models.CharField(max_length = 50,default = 'student')#teacher or student
    email = models.EmailField(blank=True)


    def __unicode__(self):
        return self.username


    class Meta:
        ordering = ['username']


class Student(models.Model):
    stu_username = models.CharField(max_length = 50)
    stu_password = models.CharField(max_length = 50)
    stu_email =  models.EmailField(blank=True)


    def __unicode__(self):
        return self.stu_username


    #set the specific order
    class Meta:
        ordering = ['stu_username']



class Group(models.Model):
    name = models.CharField(max_length = 50)
    desc = models.TextField(max_length= 100,null=True,blank=True)
    teacher = models.ForeignKey(User)
    stuCount = models.IntegerField()
    student = models.ManyToManyField(Student)
    created_at = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return u'gname=%s,teacher=%s' % (self.name,self.teacher)
#

#
#


#The db stores all VMimages in repo,both public repo and private repo(data from openstack)
class VMImage(models.Model):
    image_id = models.CharField(max_length = 36,null=True,blank=True)
    name = models.CharField(max_length = 255)
    owner = models.ForeignKey(User)
    own_project = models.CharField(max_length= 32,null=True)
    is_public = models.CharField(max_length = 10,default = 'YES')

    description = models.TextField(max_length=500,blank=True)
    status = models.CharField(max_length = 30,default = 'active')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True,null=True,blank = True)
    size = models.BigIntegerField()
    min_disk = models.IntegerField(default = 0)
    min_ram = models.IntegerField(default = 0)
    tags = models.ManyToManyField('Tag')
    is_shared = models.BooleanField(default=False)
    shared_time = models.DateTimeField(auto_now=True, null=True,editable=True)
    flavor = models.CharField(max_length= 10,null = True,blank = True,default='m1.tiny')
    keypair = models.CharField(max_length= 20,null = True,blank = True,default='mykey')

    def __unicode__(self):
        return u'name=%s,creater=%s,is_shared=%s' % (self.name,self.owner,self.is_shared)

    class Meta:
        ordering = ['-created_at']



#this is a tag system for my own platform:targetMachine, operateMachine,commonMachine
class Tag(models.Model):
    name = models.CharField(max_length = 50)
    createtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
# #






#The db table used to store required network info(from openstack)+some system data
class Network(models.Model):
    network_name = models.CharField(max_length=100)
    network_description = models.TextField(blank=True)
    subnet_name = models.CharField(max_length=50, null=True)
    ip_version = models.CharField(max_length=2, null=True,default='4')
    cidr = models.CharField(max_length=40, null=True)
    gateway_ip = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    owner = models.ForeignKey(User,null=True)#
    is_shared = models.BooleanField(default=False)
    shared_time = models.DateTimeField(auto_now=True, null=True, editable=True)
    #after finishing creation, fill below fields
    network_id = models.CharField(max_length=50, null=True, blank=True)
    subnet_id = models.CharField(max_length=50, null=True, blank=True)
    tenant_id = models.CharField(max_length=50,null=True,blank=True)
    allocation_pools_start = models.CharField(max_length=30,null=True,blank=True)
    allocation_pools_end = models.CharField(max_length=30, null=True, blank=True)
    enable_dhcp = models.CharField(max_length=10,null=True,blank=True)


    def __unicode__(self):
        return u'name=%s,creator=%s,is_shared=%s' % (self.network_name,self.owner,self.is_shared)

    class Meta:
        ordering = ['-created_at']



# #The db used to store exp template
class Experiment(models.Model):
    #basic info
    exp_name = models.CharField(max_length = 150)
    exp_description = models.TextField(blank = True)
    exp_createtime = models.DateTimeField(auto_now_add = True,editable = True)
    exp_updatetime = models.DateTimeField(auto_now = True,blank = True)#the default value is equal to created_time
    exp_owner = models.ForeignKey(User)
    #exp template
    #image_name1,image_name2,....all images contained in the exp
    exp_images = models.ManyToManyField(VMImage)#???
    exp_image_count = models.IntegerField(null=True)
    exp_network = models.ManyToManyField(Network)
    exp_guide = models.TextField(null=True,blank = True)
    exp_result = models.CharField(max_length = 500,null=True,blank = True)
    exp_reportDIR =  models.CharField(max_length = 150,null=True,blank = True)#??
    # is_shared  = models.CharField(max_length=10,null=True,default='False')
    is_shared = models.BooleanField(default=False)
    shared_time = models.DateTimeField(null=True,blank=True,editable=True)


    def __unicode__(self):
        return u'id=%s,name=%s,creater=%s,is_shared=%s' % (self.id,self.exp_name,self.exp_owner,self.is_shared)

    class Meta:
        ordering = ['-exp_createtime']



# The db table used to store chosen VMImages info by user--#relation table
class ImageCart(models.Model):
    user = models.ForeignKey(User)
    image_id = models.ForeignKey(VMImage)
    createtime = models.DateTimeField(auto_now_add=True, editable=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-createtime']



# relation table
class NetworkCart(models.Model):
    user = models.ForeignKey(User)
    network_id = models.ForeignKey(Network)
    createtime = models.DateTimeField(auto_now_add=True, editable=True)

    def __unicode__(self):
        return self.createtime

    class Meta:
        ordering = ['-createtime']



# The db table used to store exp instance info
class ExpInstance(models.Model):
    expInstance_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,max_length=200)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True, null=True, blank=True)
    creator = models.CharField(max_length=201)
    servers = models.CharField(max_length=100)  # VMInstance id
    sourceExpTemplate = models.ForeignKey(Experiment)

    def __unicode__(self):
        return u'%s %s %s' % (self.expInstance_id, self.name, self.createtime)

    class Meta:
        ordering = ['-createtime']
        #


#The db table used to store VM instance contained in the exp(data from openstack)
class VMInstance(models.Model):
    server_id = models.CharField(max_length = 100)
    name = models.CharField(max_length = 255)
    owner = models.CharField(max_length= 20)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length = 20)
    ip = models.CharField(max_length = 20,blank = True)
    vncurl = models.URLField()
    exp = models.ForeignKey(ExpInstance)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-createtime']




#
# # # #a relation table between exp and user
class Delivery(models.Model):
    name = models.CharField(max_length =100,default='delivery_record')
    desc = models.TextField(max_length=200,null=True,blank=True)
    exp = models.ForeignKey(Experiment)
    teacher = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    delivery_time = models.DateTimeField(auto_now_add = True,editable = True)
    update_time = models.DateTimeField(auto_now =True,blank=True,null=True,editable=True)
    start_time = models.DateField(editable = True,null=True,blank=True)#set when student can start the expriment
    stop_time = models.DateField(editable = True,null=True,blank=True)  # set when student should finish the expriment
    total_stu = models.IntegerField(default=0)
    undo_count = models.IntegerField(default=0)
    doing_count = models.IntegerField(default=0)
    done_count = models.IntegerField(default=0)
    average_time = models.CharField(max_length=100,null=True,blank=True)
    average_score = models.DecimalField(null=True,blank=True,max_digits=5,decimal_places=2,editable=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-delivery_time']




class Score(models.Model):
    exp = models.ForeignKey(Experiment)
    stu = models.ForeignKey(Student)
    scorer = models.ForeignKey(User)
    delivery_id = models.IntegerField(null=True,blank=True)
    createTime = models.DateTimeField(auto_now_add=True, editable=True)
    startTime = models.DateTimeField(null=True,blank=True,editable=True)
    finishedTime = models.DateTimeField(null=True,blank=True,editable=True)
    score = models.IntegerField(editable=True,default=0)
    scoreTime = models.DateTimeField(null=True,blank=True,editable=True)
    comment = models.TextField(max_length=500,null=True,blank=True)
    times = models.IntegerField(default=0)#how many times stu do this exp
    situation = models.CharField(max_length=10,default='undo')#['undo','doing','done','scored','paused']
    result = models.CharField(max_length=500,null=True,blank=True)
    result_exp_id = models.CharField(max_length=10,null=True,blank=True)#put the saved exp result(as exp_template format)
    reportUrl = models.URLField(null=True,blank=True)
