
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
        rf = AddGroupForm()
    return render_to_response("group_edit.html", {'rf': gf})


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