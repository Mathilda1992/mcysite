#This page just include those data wanted to be show on home.html

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404
from django.template import Context
from django.http import HttpResponseRedirect
#from django.core.context_processors import csrf
from django import forms
from django.http import Http404

from django.core.mail import send_mail
from django.core.mail import send_mass_mail

import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


from Iserlab import createconn_openstackSDK
from Iserlab import image_resource_operation,compute_resource_operation,network_resource_operation,identity_resource_operation
from Iserlab import experiment_operation,repo_operation,user_operation
from Iserlab import showTime

#-------import models---------
from Iserlab.models import User,Group,Student,Experiment,VMImage,Network,Delivery


auth_username = 'admin'
auth_password = 'os62511279'
auth_url = 'http://202.112.113.220:5000/v2.0/'
project_name = 'admin'
region_name = 'RegionOne'


system_admin_email = 'machenyi2011@163.com'


def home(request):
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    return render(request,'home.html',context)


def stu_home(request):
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())
    #default show the grouplist
    username = request.session['username']
    print username
    teacher = User.objects.get(username = username)
    g_list = Group.objects.filter(teacher= teacher).order_by('-created_at')

    context['GroupList'] = g_list
    return render(request,'stu_managment.html',context)


def exp_home(request):
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())
    #default show exp list
    username = request.session['username']
    role = request.session['role']
    if role=='teacher':
        teacher = User.objects.get(username=username)
        ExpList = Experiment.objects.filter(exp_owner=teacher).order_by('-exp_createtime')
        # print dir(ExpList[0])
        context['ExpList'] = ExpList
        pass
    else:#this is a student user
        pass
    return render(request,'exp_managment.html',context)


def repo_home(request):
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    # default show exp list in public repo
    username = request.session['username']
    role = request.session['role']
    if role =='teacher':
        PublicExpList = Experiment.objects.filter(is_shared='True').order_by('-shared_time')
        context['PublicExpList']=PublicExpList
    else:
        pass

    return render(request,'resource_managment.html',context)


def teach_home(request):
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    #default show the delivery history
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        teacher = User.objects.get(username=username)
        DeliveryList = Delivery.objects.filter(teacher=teacher).order_by('-delivery_time')
        context['DeliveryList'] = DeliveryList

    else:
        student = Student.objects.get(username=username)

    return render(request,'teacher_center.html',context)



#***********************************************************************#
#                  Delivery Operate/Teaching center operate                             #
#***********************************************************************#
def delivery_detail(request,d_id):
    pass


def delivery_edit(request,d_id):
    pass


def delivery_delete(request,d_id):
    try:
        d = Delivery.objects.get(id=d_id)
    except Delivery.DoesNotExist:
        raise Http404
    re = Delivery.objects.filter(id=d_id).delete()
    if re:
        print "Delivery delete success!"
    return HttpResponseRedirect('/teach_home/')



def group_delete(request,group_id):
    try:
        g = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise Http404

    # delete from db
    result = Group.objects.filter(id=group_id).delete()
    if result:
        print "group delete success!"
    return HttpResponseRedirect('/stu_home/')


def delivery_create(request):
    pass


def delivery_list_by_teacher():
    pass


def delivery_list_by_student():
    pass




#***********************************************************************#
#                 repo management operate function                     #
#***********************************************************************#
def repo_public_image_list(request):
    pass


def repo_private_list(request):
    username = request.session['username']
    teacher = User.objects.get(username=username)
    PrivateExpList = Experiment.objects.filter(exp_owner=teacher).order_by('-exp_createtime')
    context={}
    context['PrivateExpList'] = PrivateExpList
    return render(request,"repo_private_list.html",context)


def repo_private_image_list(request):
    pass


def repo_upload_image(request):
    pass



#***********************************************************************#
#                 other  function                     #
#***********************************************************************#
#----------------------------------------------------------------------------
#!!!!!!!important!!!!!!
from django.template.loader import get_template
def test_template(request):
    c = Context({'person_name':'machenyi',
                 'company':'Renmin University of China',
                 'ship_date':datetime.date(2016,12,22),
                 'item_list':['alice','bob','cara'],
                 'ordered_warranty':False})

    # t = get_template('test222.html')
    # html = t.render(c)
    # return HttpResponse(html)

    # return render(request,'test222.html',c)

    return render_to_response('test222.html',c)



def current_datetime(request):
    now = datetime.datetime.now()
    print now
    return render_to_response('test333.html',{'current_date':now})



def hours_ahead(request,offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours = offset)

    return render_to_response('test444.html',{'offset':offset,'next_time':dt})


"""
def conn_openstack(request):
    conn=createconn.create_conn()
    print "The conn object is:", conn
    context = {}
    context['hello'] = 'welcome to my platfowm'
    context['message1'] = 'Start connecting OpenStack'

    # output the conn result
    # actually this can not be used as condition
    # because failed conn also return a conn string
    if conn:
        context['conn_result'] = 'Connect OpenStack Successfully!'
    else:
        context['conn_result'] = 'Connect OpenStack Fail!'
    return HttpResponse("Hello world ! conn_openstack()")
"""

#***********************************************************************#
#                 user management operate function                     #
#***********************************************************************#
# def group_list(request):
#     g_list = user_operation.list_group()
#     context = {}
#     context['GroupList'] = g_list
#     return render(request,"stu_managment.html",context)

def group_view(request,group_id):
    try:
        g = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise Http404
    #get group details from db
    t = g.teacher
    s_list = g.student.all()
    G_Detail_Dict = {'id':g.id,'created_at':g.created_at,'name': g.name, 'desc': g.desc, 'teacher': t, 'stulist': s_list, 'stucount': g.stuCount}
    print G_Detail_Dict

    #output the group detail-----------------------------UI--------------------------
    c = {}
    c['G_Detail_Dict']=G_Detail_Dict
    return render(request,'group_detail.html',c)



STU_CHECKBOX_CHOICES=(
    ('lilei','lilei'),
    ('alice','alice'),
    ('mcy','mcy')
)

def validate_gname(gname):
    if gname == "group1":
        raise ValidationError('%s is used, please change another group name!' % gname)


class AddGroupForm(forms.Form):
    gname = forms.CharField(label='Gname',max_length=50,error_messages={'required': 'The username can not be null!','max_length':'The group name is too long'},validators=[validate_gname])
    desc = forms.CharField(label='Gdesc',max_length=500,widget=forms.Textarea(),required=False,initial="Replace with your feedbace",error_messages={'max_length':'The description is too long'})
    stulist = forms.MultipleChoiceField(label='Stulist',required=False,widget=forms.CheckboxSelectMultiple,choices=STU_CHECKBOX_CHOICES,)



def group_create(request):
    #get input from UI-----------------------UI---------------------------------
    username = request.session['username']
    if request.method == 'POST':
        rf = AddGroupForm(request.POST)
        if rf.is_valid():
            #get data from form
            gname = rf.cleaned_data['gname']
            desc = rf.cleaned_data['desc']
            stuNamelist = rf.cleaned_data['stulist']

            #insert into db
            gteacher = User.objects.get(username=username)
            stulist = []
            for i in range(0,len(stuNamelist)):
                stu = Student.objects.get(stu_username=stuNamelist[i])
                stulist.append(stu)
            gcount = len(stuNamelist)

            g = Group(name=gname, desc=desc, teacher=gteacher, stuCount=gcount)
            g.save()
            for stu in stulist:
                g.student.add(stu)

            #refresh the group list
            return HttpResponseRedirect('/stu_home/')
    else:
        rf = AddGroupForm()
    return render_to_response("group_create.html", {'rf': rf})



def group_edit(request,group_id):
    g = Group.objects.get(id=group_id)
    print g
    s_list = g.student.all()
    s_name_list = []
    for item in s_list:
        s_name_list.append(item.stu_username)

    #initial the form
    attrs = {}
    attrs['gname']=g.name
    attrs['desc']=g.desc
    attrs['stulist']= s_name_list
    gf = AddGroupForm(initial=attrs)

    #edit and update the group
    username = request.session['username']
    if request.method == 'POST':
        rf = AddGroupForm(request.POST)
        if rf.is_valid():
            # get data from form
            update_gname = rf.cleaned_data['gname']
            update_desc = rf.cleaned_data['desc']
            update_stuNamelist = rf.cleaned_data['stulist']

            # edit basic info of group
            gteacher = User.objects.get(username=username)
            update_stulist = []
            for i in range(0, len(update_stuNamelist)):
                stu = Student.objects.get(stu_username=update_stuNamelist[i])
                update_stulist.append(stu)
            update_gcount = len(update_stuNamelist)

            re =Group.objects.filter(id=group_id).update(name=update_gname,desc=update_desc,stuCount=update_gcount)
            update_g = Group.objects.get(id=group_id)
            print "********before stu update"
            print update_g

            #edit stu list of group
            for i in range(0,len(update_stulist)):
                if update_stulist[i] not in s_list:#add the stu in new list but not in old list
                    update_g.student.add(update_stulist[i])
            for j in range(0,len(s_list)):
                if s_list[j] not in update_stulist:#delete the stu in old list but not in new list
                    update_g.student.remove(s_list[j])
            print "********after stu update"
            print update_g

            # refresh the group list
            return HttpResponseRedirect('/stu_home/')
    else:
        rf = AddGroupForm()
    return render_to_response("group_edit.html", {'rf': gf})



def group_delete(request,group_id):
    username=request.session['username']

    try:
        g = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise Http404

    # delete from db
    gteacher = User.objects.get(username=username)
    result = Group.objects.filter(id=group_id).delete()
    if result:
        print "group delete success!"

    return HttpResponseRedirect('/stu_home/')



# def group_stu_get(request):
#     #get the target gname-----------------UI------------------
#     g_name = 'group2'
#
#     #get stu data from db
#     # stu_list = user_operation.get_group_stu(g_name)
#     g = Group.objects.get(name = g_name)
#     stulist = g.student.all()
#     print dir(stulist[0])
#
#     #output the result-------------------UI--------------------
#     context = {}
#     context['G_Stu_List'] = stulist
#     return render(request,"group_stu_list.html",context)



def group_get(request):
    currentuser = 'teacher1'
    teacher = user_operation.find_user(currentuser)
    glist = user_operation.get_group(teacher)
    return HttpResponse('Get current user group')



# def openstack_user_list(request):
#     conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
#     users = identity_resource_operation.list_users(conn)
#     print '***show the OpenStack Users info:***'
#
#     return HttpResponse('List openstack users')


def openstack_user_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    UserList = identity_resource_operation.list_users(conn)
    c = Context({'UserList': UserList})
    return render(request, 'image_list.html', c)



def openstack_project_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    ProjectList = identity_resource_operation.list_projects(conn)
    c = Context({'UserList': ProjectList})
    return render(request, 'image_list.html', c)



def openstack_project_find(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    project = identity_resource_operation.find_project(conn,'admin')
    return HttpResponse('Find openstack projects')



def openstack_project_create(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    dict = {}
    dict.setdefault('a',1)
    dict.setdefault('b',2)
    dict.setdefault('c',3)
    print dict
    new_project = identity_resource_operation.create_project(conn,**dict)
    return HttpResponse('Create openstack projects')



def openstack_role_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    roles = identity_resource_operation.list_roles(conn)
    return HttpResponse('List openstack roles')



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~List openstack  resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def flavor_list(request):
    # create conn to openstack
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    # define sth used to deliver to html
    FlavorList = []
    # get flavor data from openstack
    flavors = compute_resource_operation.list_flavors(conn)
    print '***show the flavors:***'
    for flavor in flavors:
        print flavor
        #extract flavor info to a dict

        FlavorList.append(flavor)

    print '**show the type of list object:**'
    print type(FlavorList[0])
    # the type of the list object :< class 'openstack.compute.v2.flavor.FlavorDetail'>

    c = Context({'FlavorList': FlavorList})
    return render(request, 'image_list.html', c)



def network_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    # define sth used to deliver to html

    NetworkList = network_resource_operation.list_networks2(conn)
    return render(request, 'image_list.html', {'NetworkList': NetworkList})



def subnet_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    s_dict_list = network_resource_operation.list_subnets(conn)
    return HttpResponse('List subnets')



def server_list(request):
    # create conn to openstack
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    # define sth used to deliver to html
    ServerList = []
    ServerList = compute_resource_operation.list_servers(conn)

    return render(request, 'image_list.html', {'ServerList': ServerList})


#list all image
def image_list(request):
    #create conn to openstack
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)

    ImageList = []
    #get images data from openstack
    ImageList = image_resource_operation.list_images(conn)

    #insert data into tables in mysql

    #output the image name list in console
    context = {}
    context["ImageList"] = ImageList

    # for i in range(0, list.__len__()):
    #     print
    return render(request,'image_list.html',context)



#The second way to get image
import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient
import os
def get_keystone_creds():
    d = {}
    d['username'] = "admin"
    d['password'] = "os62511279"
    d['auth_url'] = "http://202.112.113.220:5000/v2.0/"
    d['tenant_name'] = "admin"
    return d

def image_list2(request):
    creds = get_keystone_creds()
    keystone = ksclient.Client(**creds)
    glance_endpoint = keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
    glance = glclient.Client(glance_endpoint, token=keystone.auth_token)
    images = glance.images.list()

    ImageList = []
    # put the images into a List
    for image in images:
        ImageList.append(image)


    print "*****************8"
    print image.keys()
    print "*****************9"
    #put the imageKey into a list
    ImageKeyList = []
    for character in image.keys():
        #print character
        ImageKeyList.append(character)


    # return render(request, 'image_list.html', {'ImageKeyList': image.keys()})
    return render(request,'image_list.html',{'ImageList':ImageList})
    # return render(request, 'image_list.html', {'ImageInfo_dict':image})



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Find resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def image_find(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    image_name = 'cirros'
    compute_resource_operation.find_image(conn,image_name)
    return 'Find image by name!'


def network_find(request):
    pass



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delete resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def image_delete(request):
    pass



def network_delete(request):
    pass



def server_delete(request):
    pass


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def VM_create(request):
    #use local var
    auth_username = 'demo'
    auth_password = 'os62511279'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'demo'
    region_name = 'RegionOne'

    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    print auth_username
    print auth_password
    server_name = 'demo-alice-cirros1'
    image_name ='cirros'
    flavor_name = 'm1.tiny'
    network_name = 'private_alice'
    private_keypair_name = 'mykey'
    print 'before into ******'
    VM_ip = compute_resource_operation.create_server2(conn, server_name, image_name, flavor_name, network_name,private_keypair_name)
    print 'The cerated VM has ip: %s' % VM_ip
    return HttpResponse('VM create Success!')





def image_create(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    #Get the uploaded image file name
    image_name = upload_imageFile()#???????
    image_resource_operation.upload_image(conn,image_name)
    # List current image list
    ImageList = image_resource_operation.list_images(conn)


    c = Context({'ImageList': ImageList})
    return render(request, 'image_list.html', c)




def network_create(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    network_name = 'mcy-network222'
    subnet_name = 'mcy-subnet222'
    ip_version = '4'
    cidr = '10.0.5.0/24'
    gateway_ip = '10.0.5.1'
    description='test network'
    username = 'teacher2'
    creator = experiment_operation.get_currentuser(username)
    is_shared = 'False'
    n = network_resource_operation.create_network(conn,network_name,subnet_name,ip_version,cidr,gateway_ip,description,creator,is_shared)
    return HttpResponse('Create new network!')




#***********************************************************************#
#                          system exp  operate function         #
#***********************************************************************#

# def exp_list(request):
#     expList = experiment_operation.list_experiment()
#     c = Context({'expList':expList})
#     return render_to_response('image_list.html',c)

def exp_filter_by_user(request):
    currentuser = 'teacher2'
    elist = experiment_operation.filter_experiment_by_user(currentuser)
    c = Context({'expList': elist})
    return render_to_response('image_list.html', c)



#only role = teacher has this function
def exp_copy(request,exp_id):
    #get input form user interface
    input_exp_id = 1
    current_username = 'teacher2'
    e = experiment_operation.copy_experiment(input_exp_id,current_username)
    return HttpResponse('copy an exp')


#only role = teacher has this function
def exp_create(request):
    #get paras from UI interface
    exp_name = 'new_create_exp555'
    owner_name = 'teacher1'
    networkNameList = ['private_alice']
    description = 'this is a copy one'
    guide = 'hello'
    result = 'hello'
    reportDIR = 'hello'
    imageNameList = ['cirros','cirros-111']
    image_count = len(imageNameList)
    is_shared = False

    owner = experiment_operation.get_currentuser(owner_name)
    imagelist = []
    for i in range(0,len(imageNameList)):
        image = repo_operation.get_VMImage(imageNameList[i])
        imagelist.append(image)
    networklist = []
    for i in range(0,len(networkNameList)):
        network = repo_operation.get_network(networkNameList[i])
        networklist.append(network)
    exp = experiment_operation.create_experiment(exp_name,owner,imagelist,image_count,networklist,is_shared,description,guide,result,reportDIR)
    print 'The new created exp is:'
    print exp
    return HttpResponse('create new exp !')

#only role = teacher has this function
def exp_edit(request,exp_id):
    pass


#only role = teacher has this function
def exp_share(request,exp_id):
    pass


#only role = teacher has this function
def exp_delivery(request,exp_id):
    pass


#only role = teacher has this function
def exp_delete(request,exp_id):
    username = request.session['username']
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404

    result = Experiment.objects.filter(id=exp_id).delete()
    if result:
        print "delete exp success!"

    return HttpResponseRedirect('/exp_home/')


#teacher and stu different
def exp_detail(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404

    #get exp detail info from db
    E_Detail_Dict = experiment_operation.view_experiment_detail(exp_id)

    # output the group detail-----------------------------UI--------------------------
    c = {}
    c['E_Detail_Dict'] = E_Detail_Dict
    return render(request, 'exp_detail.html', c)


#teacher and stu different
def exp_launch(request,exp_id):
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        pass
    else:
        pass



def exp_network_launch(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    e_id = 1
    experiment_operation.luanch_exp_network(conn,e_id)
    return HttpResponse('launch exp network!')


def exp_vm_launch(request):
    pass




#***********************************************************************#
#                  Teacher add student user                             #
#***********************************************************************#
#Models: Student
def create_stu(username,password,email=' '):
    #db operation:insert a new record
    #--------------------------
    return username

#check the student list
def get_stu():
    stu_List=[]
    #db operation: get stu name list from db
    #--------------------------

    return stu_List

def add_stu(request):
    username = 'stu1'
    password = 'stu1'
    email = 'machenyi2011@163.com'

    create_stu(username,password,email)
    stu_List=[]
    stu_List=get_stu()

    #show the stuList in html page
    #----------------------

    return HttpResponse('Add Student Successfully!')








#***********************************************************************#
#                  Teacher use experiment template in repo               #
#***********************************************************************#
#Models: Experiment_Template

#List all experiments_template in public repo
def repo_exp_list(request):
    expList = experiment_operation.filter_experiment_by_shared()
    c = Context({'expList':expList})
    return render_to_response('image_list.html',c)


#Select needed experiment_template and copy another
##step1:choose one template and look into the details++++++++++++++++++++++++++++++++++++need to focus on UI+++++++++++++++++++=



##step2:make a copy



#Launch exp instance based on this template




#Modify exp template in private repo


#Delete exp template in private repo



##


#***********************************************************************#
#                  Teacher use VMImage resource in repo                 #
#***********************************************************************#
#Models:VMImage(id,name,owner,is_public,created_time)
def repo_image_list(request):
    pass



def repo_network_list(request):
    pass


#***********************************************************************#
#                  Teacher upload  VMImage to private repo              #
#***********************************************************************#
#Models:VMImage

#upload the image file to system specific dir:controller:/tmp/images/, can use scp command
def upload_imageFile():
    image_name='Uploaded_Image_Name'
    print 'Upload image file %s successfully!' % image_name
    return image_name









#***********************************************************************#
#                  Teacher shares  VMImage to VMImage repo              #
#***********************************************************************#
#




#***********************************************************************#
#                  Teacher custom create an Experiment instance         #
#***********************************************************************#



#Prepare Images
#insert into VMImage




#Create exp template
#insert into Network
#insert into Experiment

#launch exp instance


#save exp







# **********************************************************************#
#              Teacher saves experiment as template                  #
#***********************************************************************#
#Models:SaveResords:<exp_ID,operator,save_time>




# **********************************************************************#
#              Teacher shares the experiment template to repo            #
#***********************************************************************#
#in fact, we update the record in Experiment



# **********************************************************************#
#              Delivery the experiment to students                       #
#***********************************************************************#


def delivery(request):
    #Get the experiment to be delivery


    #Get the student list to delivery
    stu_List=[]
    stu_List = list_stu()
    stu_email_List=['machenyi2011@163.com','ken911121@126.com']


    #Insert a record into db:Delivery


    #After Delivery,system should notify students by email
    send_mail('Subject here', 'Here is the message', 'machenyi2011@163.com', stu_email_List, fail_silently=False)

    return HttpResponse('Delivery Success!')


# **********************************************************************#
#              Student login the system                                 #
#***********************************************************************#


# **********************************************************************#
#              Student instance the experiment                           #
#***********************************************************************#




# **********************************************************************#
#              Student save experiment status by exporting as template   #
#***********************************************************************#



# **********************************************************************#
#              Student submit the experiment                             #
#***********************************************************************#