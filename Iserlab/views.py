
# mcy write sone test code to exercise how to use Django


from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.core.mail import send_mail

# -*- coding: utf-8 -*-

#from __future__ import unicode_literals

import json


# def index(request):
#     string = "hello world"
#     NameList = ["Alice","Bob","Cara"]
#     info_dict = {'site':'baidu.com','tag':'Search Engine','country':'China'}
#
#     List = map(str,range(100))
#     # return render(request,'test.html',{'List':List})
#
#     # return render(request,'test.html',{'info_dict':info_dict})
#     stu_email_List = ['machenyi2011@163.com']
#     send_mail('Subject here', 'Here is the message', 'machenyi2011@163.com', stu_email_List, fail_silently=False)
#
#     var =87
#     return render(request, 'test.html', {'var':var})


def add(request):
    # a = request.GET['a']
    # b = request.GET['b']
    a = request.GET.get('a',0)
    b = request.GET.get('b', 0)
    c = int(a)+int(b)

    return HttpResponse(str(c))


def add2(request,a,b):
    c = int(a)+int(b)
    return HttpResponse(str(c))


def old_add2_redirect(request,a,b):
    return HttpResponseRedirect(
        reverse('add2',args=(a,b))
    )


# def home(request):
#     List = ['alice', 'bob','cara']
#     Dict = {'site': 'www.baidu.com', 'author': 'machenyi'}
#     return render(request, 'test111.html', {
#         'List': json.dumps(List),
#         'Dict': json.dumps(Dict)
#     })

#----------------------2017-2-28----------#
from .forms import AddForm
def index(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a)+int(b)))
    else:
        form = AddForm()
        return render(request,'index.html',{'form':form})


#-------------------2017-3-7---------------------#

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

    s_list = g.student.all()
    s_name_list = []
    for item in s_list:
        s_name_list.append(item.stu_username)


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


            #edit stu list of group
            for i in range(0,len(update_stulist)):
                if update_stulist[i] not in s_list:#add the stu in new list but not in old list
                    update_g.student.add(update_stulist[i])
            for j in range(0,len(s_list)):
                if s_list[j] not in update_stulist:#delete the stu in old list but not in new list
                    update_g.student.remove(s_list[j])


            # refresh the group list
            return HttpResponseRedirect('/stu_home/')
    else:
        # initial the form
        attrs = {}
        attrs['gname'] = g.name
        attrs['desc'] = g.desc
        attrs['stulist'] = s_name_list
        gf = AddGroupForm(initial=attrs)
    return render_to_response("group_edit.html", {'rf': gf})


#only role = teacher has this function
def exp_create(request):
    username = request.session['username']
    t = User.objects.get(username=username)

    if request.method == 'POST':
        guideFile = request.FILES.get("guide_file",None)
        if not guideFile:
            return HttpResponse("no file to choose")
            # messages.error(request,"no file to choose")
        save_path = "/home/mcy/upload/files"
        destination = open(os.path.join(save_path,guideFile.name),'wb+')
        for chunk in guideFile.chunks():
            destination.write(chunk)
        destination.close()

        rf = AddExpForm(request.POST)
        # if rf.is_valid():
        #get input data from form
        name = rf.data['name']
        desc = rf.data['desc']
        images_idList = rf.data['images_idList']
        networks_idList = rf.data['networks_idList']
        guide = rf.data['guide']
        refer_result=rf.data['refer_result']
        #get images
        imageList=[]
        for i in images_idList:
            imageList.append(VMImage.objects.get(id=i))
        networkList=[]
        for i in networks_idList:
            networkList.append(Network.objects.get(id=i))
        #get networks
        exp_guide_path = save_path+'/'+guideFile.name
        e = Experiment(exp_name=name,exp_description=desc,exp_owner=t,exp_image_count=len(imageList),
                       exp_guide=guide,exp_result=refer_result,exp_guide_path=exp_guide_path)
        e.save()
        for item in imageList:
            e.exp_images.add(item)
        for item in networkList:
            e.exp_network.add(item)

        #refresh the exp list
        return HttpResponseRedirect('/exp_home/')
    else:
        rf = AddExpForm()
    return render_to_response("exp_create.html",{'rf':rf})


def repo_create_image(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    # if request.method == 'POST':
    #     form = CreateImageForm(request.POST,request.FILES)
    #     if form.is_valid():
    #         repo_handle_upload_image()
    # pass
    if request.method =="POST":
        myfile = request.FILES.get("myfile",None)
        if not myfile:
            return HttpResponse("no file to choose")
        save_path = "/home/mcy/upload/files"
        destination = open(os.path.join(save_path,myfile.name),'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        #get data from form
        rf = CreateImageForm(request.POST)
        name = rf.data['name']
        desc = rf.data['desc']

        #insert into db
        file_path = save_path+'/'+myfile.name
        new = VMImage(name=name,description=desc,path=file_path,owner=t)
        new.save()

        # response = "congrats. your file \"" + myfile.name + "\" has been uploaded."
        return HttpResponseRedirect("/repo_home/")
    else:
        rf = CreateImageForm()
    return render(request,'repo_create_image.html',{'rf':rf})


def create_experiment(experiment_name,owner,imagelist,image_count,networklist,is_shared='False',description='description',guide='Please input exp guide here',result='Please input exp result here to refer',reportDIR='Please input report DIR here'):
    print ("Create Experiment:")
    #Insert a resocrd into db: experiment
    e1 = Experiment(
        exp_name=experiment_name,
        # exp_owner = ownerlist[owner_index],
        exp_owner = owner,
        exp_image_count = image_count,
        exp_description = description,
        exp_guide = guide,
        exp_result = result,
        exp_reportDIR = reportDIR,
        is_shared = is_shared
    )
    e1.save()

    # for image_index in image_indexlist:
    #     e1.exp_images.add(imagelist[i])
    for image in imagelist:
        e1.exp_images.add(image)
    print "here is network@@@@@@@@"
    print networklist
    for network in networklist:
        e1.exp_network.add(network)
    print e1
    return e1

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


def delivery_detail(request,d_id):
    try:
        d = Delivery.objects.get(id =d_id)
    except Delivery.DoesNotExist:
        raise Http404
    #get delivery detail from db
    context = {}
    s_list = d.group.student.all()
    D_detial_dict = {'id':d_id,'name':d.name,'desc':d.desc,'exp':d.exp,'teacher':d.teacher,'group':d.group,
                     'stulist':s_list,'delivery_time':d.delivery_time,'start_time':d.start_time,
                     'stop_time':d.stop_time,'total_stu':len(s_list),
                     }
    context['D_detail_dict']=D_detial_dict
    return render(request,'delivery_detail.html',context)


#only role = teacher has this function
def exp_share(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    #update the is_shared field in Experiment db
    re = Experiment.objects.filter(id=exp_id).update(is_shared=True,shared_time=datetime.datetime.now())
    return HttpResponseRedirect('/exp_home/')


def exp_delete(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    result = Experiment.objects.filter(id=exp_id).delete()
    if result:
        print "delete exp success!"
    return HttpResponseRedirect('/exp_home/')



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



def download_file(request):
    # do something...

    #使用迭代器加载文件，实现大文件的下载
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "/home/mcy/upload/files/localrc.txt"

    #使用StreamingHttpResponse配合迭代器返回文件到页面
    response = StreamingHttpResponse(file_iterator(the_file_name))

    # 设置内容的格式使之能下载到硬盘而非显示在页面
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response


#list all image
def image_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    ImageList = image_resource_operation.list_images(conn)
    context = {}
    context["ImageList"] = ImageList
    return render(request,'image_list.html',context)


def server_create(request):
    #use local var
    auth_username = 'demo'
    auth_password = 'os62511279'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'demo'
    region_name = 'RegionOne'

    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)

    server_name = 'demo-alice-cirros2'
    image_name ='cirros'
    flavor_name = 'm1.tiny'
    network_name = 'private_alice'
    private_keypair_name = 'mykey'
    print 'before into ******'
    slist = compute_resource_operation.create_server2(conn, server_name, image_name, flavor_name, network_name,private_keypair_name)
    print slist[0]
    return HttpResponse('VM create Success!')


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
    n = network_resource_operation.create_network(conn,network_name,subnet_name,ip_version,cidr,gateway_ip)
    return HttpResponse('Create new network!')