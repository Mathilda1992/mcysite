#This page just include those data wanted to be show on home.html

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404
from django.template import Context
from django.http import HttpResponseRedirect
#from django.core.context_processors import csrf
from django import forms

import datetime


from Iserlab import createconn_openstackSDK
from Iserlab import image_resource_operation,compute_resource_operation,network_resource_operation,identity_resource_operation
from Iserlab import experiment_operation,repo_operation,user_operation
from Iserlab import showTime



auth_username = 'admin'
auth_password = 'os62511279'
auth_url = 'http://202.112.113.220:5000/v2.0/'
project_name = 'admin'
region_name = 'RegionOne'


def hello(request):
    context={}
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())
    return render(request,'home.html',context)


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
#    some public openstack resource operate function                     #
#***********************************************************************#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~User related operation~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def group_list(request):
    u_list = user_operation.list_group()
    return HttpResponse('List Group!')


def group_create(request):
    gname = 'group2'
    currentuser = 'teacher1'
    stuNamelist = ['mcy','lilei']
    desc = 'hello'

    gteacher = user_operation.find_user(currentuser)
    stulist = []
    for i in range(0,len(stuNamelist)):
        stu = user_operation.find_stu(stuNamelist[i])
        stulist.append(stu)
    gcount = len(stuNamelist)

    g = user_operation.create_group(gname,gteacher,gcount,stulist,desc)
    return HttpResponse('Create Group!')


def group_delete(request):
    g_name = 'info_sec'
    user_operation.delete_group(g_name)
    return HttpResponse('Delete Group')


def group_stu_get(request):
    g_name = 'group2'
    stu_list = user_operation.get_group_stu(g_name)

    return HttpResponse('Get group stu')


def group_get(request):
    currentuser = 'teacher1'
    teacher = user_operation.find_user(currentuser)
    glist = user_operation.get_group(teacher)
    return HttpResponse('Get current user group')


def group_view(request):
    g_name = 'group2'
    g_dict = user_operation.view_group(g_name)
    return HttpResponse('Show the group details')



def openstack_user_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    identity_resource_operation.list_users(conn)
    return HttpResponse('List openstack users')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~List resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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
        FlavorList.append(flavor)

    print '**show the type of list object:**'
    print type(FlavorList[0])
    # the type of the list object :< class 'openstack.compute.v2.flavor.FlavorDetail'>

    c = Context({'FlavorList': FlavorList})
    return render(request, 'image_list.html', c)


def network_list(request):
    # create conn to openstack
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    # define sth used to deliver to html
    NetworkList = []
    # get flavor data from openstack
    networks = compute_resource_operation.list_networks(conn)
    print '***show the networks:***'
    for network in networks:
        print network
        NetworkList.append(network)
    print '**show the type of list object:**'
    print type(NetworkList[0])
    # the type of the list object :<class 'openstack.network.v2.network.Network'>
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
    # get flavor data from openstack
    servers = compute_resource_operation.list_servers(conn)
    print '***show the servers:***'
    for server in servers:
        print server
        ServerList.append(server)

    print '**show the type of list object:**'
    print type(ServerList[0])
    # the type of the list object :<class 'openstack.compute.v2.server.ServerDetail'>

    return render(request, 'image_list.html', {'ServerList': ServerList})


#list all image
def image_list(request):
    #create conn to openstack
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    #define sth used to deliver to html
    ImageList = []
    #get images data from openstack
    images = image_resource_operation.list_images(conn)

    #insert data into tables in mysql

    #output the image list in console
    print('**********List Images**************')
    for image in images:
        # print(image)
        # we should analysis the image info string into a imageInfo_dict


        #test whether the image is a string or a dict?? the object type in the list is class, <class 'openstack.image.v2.image.Image'>
        # print image

        #put the imageInfo_dict into a imageList
        ImageList.append(image)

    for j in ImageList:
        print j

    print '*********'
    print ImageList[0]


    #get the type of list object
    print '*****get the type of list object***'
    for i in range(0,ImageList.__len__()):
        print type(ImageList[i])
    #output result
    # < class 'openstack.image.v2.image.Image'>


    # list = [1, 'a', 'b', {'key': 'value'}]
    # for i in range(0, list.__len__()):
    #     print type(list[i])
    #
    # print 'stringtype:'
    # for i in range(0, list.__len__()):
    #     if isinstance(list[i], str):
    #         print type(list[i])

    return render(request,'image_list.html',{'ImageList':ImageList})



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
    images = image_resource_operation.list_images(conn)
    ImageList=[]
    for image in images:
        ImageList.append(image)
        print image

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
#                          some system public operate function         #
#***********************************************************************#

def exp_list(request):
    expList = experiment_operation.list_experiment()
    c = Context({'expList':expList})
    return render_to_response('image_list.html',c)

def exp_filter_by_user(request):
    currentuser = 'teacher2'
    elist = experiment_operation.filter_experiment_by_user(currentuser)
    c = Context({'expList': elist})
    return render_to_response('image_list.html', c)


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


def exp_update(request):
    pass



def exp_delete(request):
    pass


def exp_network_launch(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    e_id = 1
    experiment_operation.luanch_exp_network(conn,e_id)
    return HttpResponse('launch exp network!')


def exp_vm_launch(request):
    pass

#***********************************************************************#
#                  Teacher login the system                             #
#***********************************************************************#




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


def openstack_users_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    UserList = []
    users = identity_resource_operation.list_users(conn)
    print '***show the OpenStack Users:***'
    for user in users:
        print user
        UserList.append(user)

    print '**show the type of list object:**'
    print type(UserList[0])

    c = Context({'UserList': UserList})
    return render(request, 'image_list.html', c)





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
def exp_detail(request):
    input_e_id = 1
    edict = experiment_operation.view_experiment_detail(input_e_id)

    return HttpResponse('Show exp details!')


##step2:make a copy
def exp_copy(request):
    #get input form user interface
    input_exp_id = 1
    current_username = 'teacher2'
    e = experiment_operation.copy_experiment(input_exp_id,current_username)

    return HttpResponse('copy an exp')


#Launch exp instance based on this template
def exp_launch(request):
    pass






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

from django.core.mail import send_mail
from django.core.mail import send_mass_mail
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