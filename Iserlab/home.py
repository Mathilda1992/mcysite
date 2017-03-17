# -*- coding: UTF-8 -*-
#This page just include those data wanted to be show on home.html
from django.contrib import messages
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404
from django.template import Context
from django.http import HttpResponseRedirect,StreamingHttpResponse
#from django.core.context_processors import csrf
from django import forms
from django.http import Http404

from django.core.mail import send_mail
from django.core.mail import send_mass_mail

import datetime,time

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from Iserlab import createconn_openstackSDK
from Iserlab import image_resource_operation,compute_resource_operation,network_resource_operation,identity_resource_operation
from Iserlab import experiment_operation,repo_operation,user_operation
from Iserlab import showTime

#-------import models---------
from Iserlab.models import *

#-------import forms----------
from Iserlab.forms import *

#--------default argus used for connect to OpenStack Cloud----
auth_username = 'admin'
auth_password = 'os62511279'
auth_url = 'http://202.112.113.220:5000/v2.0/'
project_name = 'admin'
region_name = 'RegionOne'


system_admin_email = 'machenyi2011@163.com'

def get_auth_info(username,password):
    authDict = {}
    authDict['auth_username'] = username
    authDict['auth_password'] = password
    authDict['auth_url'] = 'http://202.112.113.220:5000/v2.0/'
    authDict['project_name']=username
    authDict['region_name']= 'RegionOne'
    return authDict
#-----------form defination--------


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

    else:#this is a student user
        student = Student.objects.get(stu_username=username)
        #list all exps those were deliveried to this student
        ScoreList = Score.objects.filter(stu=student).order_by('-createTime')
        context['ScoreList']=ScoreList
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

    #default show the exp situation list
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        teacher = User.objects.get(username=username)
        DeliveryList = Delivery.objects.filter(teacher=teacher).order_by('-delivery_time')
        context['DeliveryList'] = DeliveryList
    else:
        student = Student.objects.get(stu_username=username)
        ScoreList = Score.objects.filter(stu=student,situation='scored').order_by('-scoreTime')
        context['ScoreList']=ScoreList
        context['exp_count']=len(ScoreList)
    return render(request,'teacher_center.html',context)


def openstack_API_home(request):#default list images
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())
    return render(request,'openstack_API_home.html',context)

#***********************************************************************#
#                  Teaching center operate                             #
#***********************************************************************#
#-----------Delivery Operate(only role=teacher has these function)-------------#
def delivery_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    teacher = User.objects.get(username=username)
    DeliveryList = Delivery.objects.filter(teacher=teacher).order_by('-delivery_time')
    context['DeliveryList'] = DeliveryList
    return render(request, 'delivery_list.html', context)


def delivery_delete(request,d_id):
    try:
        d = Delivery.objects.get(id=d_id)
    except Delivery.DoesNotExist:
        raise Http404
    re = Delivery.objects.filter(id=d_id).delete()
    #also should delete related records in Score db

    if re:
        print "Delivery delete success!"
    return HttpResponseRedirect('/delivery_list/')


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


def delivery_edit(request,d_id):
    try:
        d = Delivery.objects.get(id=d_id)
    except Delivery.DoesNotExist:
        raise Http404

    #edit and update the delivery
    if request.method == 'POST':
        rf = EditDeliveryForm(request.POST)
        if rf.is_valid():
            #get data from form
            update_name = rf.cleaned_data['name']
            update_desc = rf.cleaned_data['desc']
            update_startDateTime = rf.cleaned_data['startDateTime']
            update_endDateTime = rf.cleaned_data['endDateTime']
            #update in db
            re = Delivery.objects.filter(id=d_id).update(name=update_name,desc=update_desc,start_time=update_startDateTime,
                                                         stop_time=update_endDateTime,update_time = datetime.datetime.now())
            update_d = Delivery.objects.get(id=d_id)
            return HttpResponseRedirect('/delivery_list/')
    else:
        # initial the form
        attrs = {}
        attrs['name'] = d.name
        attrs['desc'] = d.desc
        attrs['exp'] = d.exp.exp_name
        attrs['group'] = d.group.name
        attrs['startDateTime'] = d.start_time
        attrs['endDateTime'] = d.stop_time
        gf = EditDeliveryForm(initial=attrs)
    return render_to_response("delivery_edit.html",{'rf':gf})


#pay attention to multi exps to multi group
def delivery_create(request):
    username = request.session['username']
    teacher = User.objects.get(username=username)

    #clear the TempExp
    TempExp.objects.all().delete()
    #insert into TempExp
    EList= Experiment.objects.filter(exp_owner=teacher)
    for item in EList:
        new = TempExp(name=item.exp_name,owner=teacher)
        new.save()

    #clear the TempGroup
    TempGroup.objects.all().delete()
    #insert into TempGroup
    GList=Group.objects.filter(teacher=teacher)
    for item in GList:
        new = TempGroup(name=item.name,owner=teacher)
        new.save()

    if request.method =='POST':
        rf = AddDeliveryForm(request.POST)
        if rf.is_valid():
            print "******"
            #get data from the form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            exp_idList = rf.cleaned_data['exp']
            group_idList = rf.cleaned_data['group']
            startDateTime = rf.cleaned_data['startDateTime']
            endDateTime = rf.cleaned_data['endDateTime']
            #prepare other required data

            delivery_time = datetime.datetime.now()

            elist = []
            glist = []
            for i in range(0,len(exp_idList)):
                e = Experiment.objects.get(id=exp_idList[i])
                elist.append(e)
            for i in range(0,len(group_idList)):
                g = Group.objects.get(id = group_idList[i])
                glist.append(g)
            # insert into db:delivery
            for i in range(0,len(elist)):
                for j in range(0,len(glist)):
                    stulist = glist[j].student.all()
                    d = Delivery(name=name,desc=desc,delivery_time=delivery_time,teacher=teacher,
                                 start_time=startDateTime,stop_time=endDateTime,
                                 exp=elist[i],group=glist[j],total_stu=len(stulist))
                    print d
                    d.save()
            #insert into db:score
            d_List = Delivery.objects.filter(name=name,teacher=teacher)
            for i in range(0,len(d_List)):
                stulist = d_List[i].group.student.all()
                for j in range(0,len(stulist)):#insert a record into score db for every stu
                    new_score = Score(exp=d_List[i].exp,stu=stulist[j],scorer= teacher,delivery_id=d_List[i].id)
                    print new_score
                    new_score.save()
        return HttpResponseRedirect('/delivery_list/')
    else:
        rf = AddDeliveryForm()
    return render_to_response("delivery_create.html",{'rf':rf})


def delivery_list_by_teacher():
    pass




#----------teaching situation operation------------#
def teach_situation_detail_by_scoreID(request,score_id):#??????
    pass



def teach_situation_detail_by_delivery(request,d_id):
    request.session['delivery_id'] = d_id
    print "************set session******"
    try:
        d = Delivery.objects.get(id = d_id)
    except Delivery.DoesNotExist:
        raise Http404
    # get data from delivery db
    t = d.teacher
    g = d.group
    print g.name
    e = d.exp
    stu_list = g.student.all()

    # list =[]
    # for stu in stu_list:
    #     #get data from score db
    #     score = Score.objects.get(stu=stu,exp=e,scorer=t,delivery_id=d_id)
    #     list.append(score)
    ScoreList = Score.objects.filter(delivery_id=d_id)
    context={}
    context['Delivery'] = d
    context['ScoreList'] = ScoreList

    return render(request,'teach_situation_detail_by_delivery.html',context)



#-----score how this stu do this exp
def teach_result_score(request,score_id):
    #initial the form
    s = Score.objects.get(id=score_id)
    print s.score
    print s.comment
    attrs = {}
    attrs['score']=s.score
    attrs['comment']=s.comment
    rf = ScoreForm(initial=attrs)

    username = request.session['username']
    print request.method
    if request.method == 'POST':
        sf = ScoreForm(request.POST)
        #get data from form
        if sf.is_valid():
            score = sf.cleaned_data['score']
            comment = sf.cleaned_data['comment']

            #update into db
            re = Score.objects.filter(id=score_id).update(situation='scored',score=score,comment=comment,scoreTime = datetime.datetime.now())
            if re:
                print "Score Success!"
            return HttpResponseRedirect('/teach_result_list/')
    else:
        sf = ScoreForm()
    return render_to_response("teach_result_score.html", {'sf': rf})



def teach_result_report_download(request,score_id):
    try:
        s = Score.objects.get(id=score_id)
    except Score.DoesNotExist:
        raise Http404
    if s.report_path:
        response = StreamingHttpResponse(file_iterator(s.report_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(s.report_path)
        return response
    else:
        return HttpResponse("Report does not exist!")


#---list all exp results(situation=done)-----from score db
def teach_result_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    current_teacher = User.objects.get(username=username)
    ResultList = Score.objects.filter(scorer=current_teacher,situation='Done').order_by('-finishedTime')
    context['ResultList'] = ResultList
    return render(request, 'teach_result_list.html', context)



#equal to teach_score_list_by_exp
def teach_score_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    #default show scores by exp(distinct)
    username = request.session['username']
    t = User.objects.get(username=username)
    ScoreList = Score.objects.filter(scorer=t,situation='Scored')
    #get distinct exp name
    eIdList = []
    for item in ScoreList:
        eIdList.append(item.exp.id)
    distinct_eIDList = list(set(eIdList))

    ExpScoreList=[]
    #get average score for every exp,get stu list for specific exp
    for i in distinct_eIDList:
        e = Experiment.objects.get(id=i)
        a_list = Score.objects.filter(scorer=t,exp=e,situation="scored").order_by('-scoreTime')
        e_totalscore = 0
        e_stulist = []
        for i in a_list:
            e_totalscore = e_totalscore + i.score
            e_stulist.append(i.stu)
        avescore = float(e_totalscore)/len(a_list)

        ExpScoreDict = {}
        ExpScoreDict['exp']= e
        ExpScoreDict['ave']=avescore
        ExpScoreDict['members']=len(e_stulist)
        ExpScoreDict['stulist']=e_stulist
        ExpScoreList.append(ExpScoreDict)
    context['ExpScoreList']=ExpScoreList
    return render(request,'teach_score_list.html',context)


#only role=teacher
def teach_score_list_by_stu(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    t = User.objects.get(username=username)
    ScoreList = Score.objects.filter(scorer=t, situation='Scored')
    #get distinct stu username
    stuIdList=[]
    for item in ScoreList:
        stuIdList.append(item.stu.id)
    distinct_stuIdList = list(set(stuIdList))

    StuScoreList=[]
    #get average score for every stu,get exp list for specific stu
    for i in distinct_stuIdList:
        stu = Student.objects.get(id = i)
        a_list = Score.objects.filter(scorer=t,stu=stu,situation="scored").order_by('-scoreTime')
        s_totalscore = 0
        s_explist=[]
        for i in a_list:
            s_totalscore = s_totalscore+i.score
            s_explist.append(i.exp)
        avescore = float(s_totalscore)/len(a_list)

        StuScoreDict={}
        StuScoreDict['stu']=stu
        StuScoreDict['ave']=avescore
        StuScoreDict['exp_count']=len(s_explist)
        StuScoreDict['explist']=s_explist
        StuScoreList.append(StuScoreDict)
    context['StuScoreList']=StuScoreList
    return render(request,'teach_score_list_by_stu.html',context)


def teach_score_list_by_group(request):
    username = request.session['username']
    stu = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=stu,situation='Scored').order_by("-scoreTime")

    group_list=[]
    for item in ScoreList:
        g = Group.objects.get(id = item.group_id)
        if g not in group_list:
            group_list.append(g)
    context = {}
    context['group_count']=len(group_list)
    GroupScoreList=[]
    for g in group_list:
        dict ={}
        dict['group']=g
        # exp_list=Delivery.objects.filter(group=g)
        total =0
        scorelist = Score.objects.filter(stu=stu,situation='scored',group_id=g.id)

        for item in scorelist:
            total = total+item.score
        if len(scorelist):
            ave_score = float(total)/len(scorelist)
        else:
            ave_score=0
        dict['ave_score']=ave_score
        dict['exp_count']=len(scorelist)
        GroupScoreList.append(dict)
    context['GroupScoreList']=GroupScoreList
    return render(request,'teach_score_list_by_group.html',context)

def teach_score_list_by_groupID(request,g_id):
    username = request.session['username']
    stu = Student.objects.get(stu_username=username)
    g = Group.objects.get(id=g_id)
    ScoreList = Score.objects.filter(stu=stu,situation='scored',group_id=g_id).order_by("-scoreTime")
    total =0
    for item in ScoreList:
        total +=item.score
    if len(ScoreList):
        ave_score = float(total)/len(ScoreList)
    else:
        ave_score=0
    context={}
    context['group']=g
    context['total_score']=total
    context['exp_count']=len(ScoreList)
    context['ave_score']=ave_score
    context['ScoreList']=ScoreList
    return render(request,"teach_score_list_by_groupID.html",context)



def teach_score_list_by_expID(request,exp_id):
    username = request.session['username']
    t =User.objects.get(username=username)
    e = Experiment.objects.get(id=exp_id)
    scores = Score.objects.filter(exp=e,situation="scored",scorer=t).order_by('-score')
    if len(scores):
    #get the ave score for the exp
        total_score = 0
        for item in scores:
            total_score+=item.score
        context = {}
        context['exp'] = e
        context['score_count'] = len(scores)
        context['total_score'] = total_score
        context['ave_score'] = float(total_score) / len(scores)
        context['ScoreList'] = scores
        render(request,'teach_score_list_by_expID.html',context)
        return render(request,'teach_score_list_by_expID.html',context)
    else:
        return HttpResponseRedirect('/teach_score_list/')

#teacher and student diff
def teach_score_list_by_stuID(request,stu_id):
    username = request.session['username']
    role = request.session['role']
    t = User.objects.get(username=username)
    s = Student.objects.get(id= stu_id)
    if role == 'teacher':
        scores = Score.objects.filter(stu=s,situation="scored",scorer=t).order_by('-finishedTime')
    else:
        scores = Score.objects.filter(stu = s,situation="scored").order_by('-finishedTime')
    if len(scores):
        #get the average score for the stu
        total_score=0
        for item in scores:
            total_score+=item.score
        context={}
        context['student']=s
        context['score_count']=len(scores)
        context['total_score']=total_score
        context['ave_score']=float(total_score)/len(scores)
        context['ScoreList']=scores
        return render(request,'teach_score_list_by_stuID.html',context)
    else:
        return HttpResponseRedirect('/teach_score_list/')

#list scores of all stus in this delivery
def teach_score_list_by_deliveryID(request,d_id):
    username = request.session['username']
    t = User.objects.get(username=username)
    d = Delivery.objects.get(id=d_id)
    scores = Score.objects.filter(delivery_id=d_id,situation="scored",scorer=t).order_by('-score')
    if len(scores):
        # get the average score
        total_score = 0
        for item in scores:
            total_score += item.score
        context = {}
        context['exp'] = d.exp
        context['score_count'] = len(scores)
        context['total_score'] = total_score
        context['ave_score'] = float(total_score) / len(scores)
        context['ScoreList'] = scores
        context['delivery_id'] = d_id
        return render(request,'teach_score_list_by_deliveryID.html',context)
    else:
        return HttpResponseRedirect('/teach_home/')

def teach_score_list_by_scoreID(request,score_id):
    pass

#***********************************************************************#
#                 repo management operate function                     #
#***********************************************************************#

def repo_ImageCart_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    t = User.objects.get(username=username)
    imageList = ImageCart.objects.filter(user=t).order_by("-createtime")
    context["CartList"] = imageList
    return render(request,"repo_ImageCart_list.html",context)



def repo_ImageCart_clear(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    result = ImageCart.objects.filter(user=t).delete()
    if result:
        print "clear th imagecart success!"
    return HttpResponseRedirect('/repo_ImageCart_list/')



def repo_ImageCart_add(request,i_id):
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404
    username = request.session['username']
    t = User.objects.get(username=username)
    cart = ImageCart.objects.filter(image=image)
    if cart:
        print "This image already in Cart!"
        return HttpResponse("This image already in Cart!")
    else:
        new = ImageCart(user=t,image=image)
        new.save()
        print "repo_ImageCart_add Success!"
        return HttpResponse("repo_ImageCart_add Success!")



def repo_NetworkCart_clear(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    result = NetworkCart.objects.filter(user=t).delete()
    if result:
        print "clear th NetworkCart success!"
    return HttpResponseRedirect('/repo_NetworkCart_list/')



def repo_NetworkCart_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    t = User.objects.get(username=username)
    networkList = NetworkCart.objects.filter(user=t).order_by("-createtime")
    context["CartList"] = networkList
    return render(request, "repo_NetworkCart_list.html", context)



def repo_NetworkCart_add(request,n_id):
    try:
        net = Network.objects.get(id=n_id)
    except Network.DoesNotExist:
        raise Http404
    username = request.session['username']
    t = User.objects.get(username=username)
    cart = NetworkCart.objects.filter(network=net)
    if cart:
        print "already in cart"
        return HttpResponse("This net already in Cart")
    else:
        new = NetworkCart(user=t,network=net)
        new.save()
        print "repo_NetworkCart_add success"
        return HttpResponse("repo_NetworkCart_add success")



def repo_ImageCart_delete(request,i_id):
    try:
        cart = ImageCart.objects.get(id=i_id)
    except ImageCart.DoesNotExist:
        raise Http404
    result = ImageCart.objects.filter(id=i_id).delete()
    if result:
        print "delete success"
    return HttpResponseRedirect('/repo_ImageCart_list/')



def repo_NetworkCart_delete(request,n_id):
    try:
        cart = NetworkCart.objects.get(id=n_id)
    except NetworkCart.DoesNotExist:
        raise Http404
    result = NetworkCart.objects.filter(id=n_id).delete()
    if result:
        print "delete success"
    return HttpResponseRedirect('/repo_NetworkCart_list/')



def repo_image_detail(request,i_id):
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404
    #get image detail from db
    context = {}
    context['username']=request.session['username']
    context['DetailDict'] = image
    return render(request,'repo_image_detail.html',context)



def repo_image_edit(request,i_id):
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        rf = EditImageForm(request.POST)
        if rf.is_valid():
            #get data from form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            re = VMImage.objects.filter(id=i_id).update(name=name,description=desc)
            #openstack API

            if re:
                messages.success(request,"Update Image Success!")
            return HttpResponseRedirect('/repo_private_image_list/')
    else:
        #initial the form
        attrs ={}
        attrs['name']=image.name
        attrs['desc']=image.description
        gf = EditImageForm(initial=attrs)
    return render_to_response("repo_image_edit.html",{'rf':gf})



def repo_image_delete(request,i_id):
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404
    result = VMImage.objects.filter(id=i_id).delete()
    #openstack API

    if result:
        print "delete success"
    return HttpResponseRedirect('/repo_private_image_list/')



def repo_image_share(request,i_id):
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404
    re = VMImage.objects.filter(id=i_id).update(is_shared=True)
    if re:
        print "repo_image_share Success!"
    return HttpResponseRedirect('/repo_private_image_list/')


def repo_network_detail(request,n_id):
    try:
        network = Network.objects.get(id=n_id)
    except Network.DoesNotExist:
        raise Http404
    #get network detail from db
    context = {}
    context['username'] = request.session['username']
    context['DetailDict'] = network
    return render(request,'repo_network_detail.html',context)


def repo_network_edit(request,n_id):
    try:
        net = Network.objects.get(id=n_id)
    except Network.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        rf = AddNetworkForm(request.POST)
        if rf.is_valid():
            # get data from form input
            name = rf.cleaned_data['name']
            subnet_name = rf.cleaned_data['subnet_name']
            desc = rf.cleaned_data['desc']
            ip_version = rf.cleaned_data['ip_version']
            cidr = rf.cleaned_data['cidr']
            gateway = rf.cleaned_data['gateway']
            allocation_pools_start = rf.cleaned_data['allocation_pools_start']
            allocation_pools_end = rf.cleaned_data['allocation_pools_end']
            enable_dhcp = rf.cleaned_data['enable_dhcp']
            #update the data in db
            re = Network.objects.filter(id=n_id).update(network_name=name,network_description=desc,subnet_name=subnet_name,
                                                        ip_version=ip_version,cidr=cidr,gateway_ip=gateway,
                                                        allocation_pools_start=allocation_pools_start,
                                                        allocation_pools_end=allocation_pools_end,enable_dhcp=enable_dhcp,
                                                        updated_at=datetime.datetime.now())
            #openstack API

            if re:
                messages.success(request,"Edit Network Success")
            return HttpResponseRedirect('/repo_private_network_list/')
    else:
        #initial the form
        attrs = {}
        attrs['name'] = net.network_name
        attrs['subnet_name'] = net.subnet_name
        attrs['network_description']=net.network_description
        attrs['ip_version']=net.ip_version
        attrs['cidr']=net.cidr
        attrs['gateway']=net.gateway_ip
        attrs['allocation_pools_start']=net.allocation_pools_start
        attrs['allocation_pools_end']=net.allocation_pools_end
        attrs['enable_dhcp']=net.enable_dhcp
        gf = AddNetworkForm(initial=attrs)
    return render_to_response("repo_network_edit.html",{'rf':gf})


def repo_network_delete(request,n_id):
    try:
        net = Network.objects.get(id=n_id)
    except Network.DoesNotExist:
        raise Http404
    re = Network.objects.filter(id=n_id).delete()
    if re:
        print "repo_image_share Success!"
    return HttpResponseRedirect('/repo_private_network_list/')


def repo_VM_detail(request,vm_id):
    try:
        vm = VM.objects.get(id=vm_id)
    except VM.DoesNotExist:
        raise Http404
    # get VM detail from db
    context = {}
    context['username'] = request.session['username']
    context['DetailDict'] = vm
    return render(request, 'repo_VM_detail.html', context)

def repo_VM_edit(request,vm_id):
    try:
        vm = VM.objects.get(id=vm_id)
    except VM.DoesNotExist:
        raise Http404
    pass

def repo_VM_delete(request,vm_id):
    try:
        vm = VM.objects.get(id=vm_id)
    except VM.DoesNotExist:
        raise Http404
    re = VM.objects.filter(id=vm_id).delete()
    if re:
        print "repo_VM_delete success"
    return HttpResponseRedirect('/repo_private_VM_list/')

#---------------------------------------------------#
def repo_public_image_delete(request,i_id):#actually this operation is to set is_shared to False
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404
    re = VMImage.objects.filter(id=i_id).update(is_shared=False)
    if re:
        print "repo_public_image_delete Success!"
    return HttpResponseRedirect('/repo_public_image_list/')



def repo_public_image_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    PublicImageList = VMImage.objects.filter(is_shared=True).order_by("-shared_time")
    context['PublicImageList']=PublicImageList
    return render(request,"repo_public_image_list.html",context)



def repo_public_exp_delete(request,e_id):
    try:
        e= Experiment.objects.get(id=e_id)
    except Experiment.DoesNotExist:
        raise Http404
    #update is_shared field to False in Experiment db
    re = Experiment.objects.filter(id=e_id).update(is_shared = False)
    if re:
        print "repo_public_exp_delete success!"
    return HttpResponseRedirect('/repo_home/')



def repo_private_exp_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    teacher = User.objects.get(username=username)
    PrivateExpList = Experiment.objects.filter(exp_owner=teacher).order_by('-exp_createtime')
    context['PrivateExpList'] = PrivateExpList
    return render(request,"repo_private_exp_list.html",context)



def repo_private_image_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    t = User.objects.get(username=username)
    PrivateImageList = VMImage.objects.filter(owner=t).order_by('-created_at')
    context['PrivateImageList']=PrivateImageList
    return render(request,"repo_private_image_list.html",context)



def repo_private_network_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    t = User.objects.get(username=username)
    NetList = Network.objects.filter(owner=t).order_by('-created_at')
    context['NetList']= NetList
    return render(request,"repo_private_network_list.html",context)

def repo_private_VM_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    t = User.objects.get(username=username)
    VMList = VM.objects.filter(owner=t).order_by('-created_at')
    context['VMList']=VMList
    return render(request,"repo_private_VM_list.html",context)



#only role=teacher
def repo_create_network(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    if request.method == 'POST':
        rf = AddNetworkForm(request.POST)
        if rf.is_valid():
            #get data from form input
            name = rf.cleaned_data['name']
            subnet_name = rf.cleaned_data['subnet_name']
            desc = rf.cleaned_data['desc']
            ip_version = rf.cleaned_data['ip_version']
            cidr = rf.cleaned_data['cidr']
            gateway = rf.cleaned_data['gateway']
            allocation_pools_start = rf.cleaned_data['allocation_pools_start']
            allocation_pools_end=rf.cleaned_data['allocation_pools_end']
            enable_dhcp=rf.cleaned_data['enable_dhcp']

            #insert into db
            n = Network(owner=t,network_name=name,network_description=desc,subnet_name=subnet_name,ip_version=ip_version,
                        cidr=cidr,gateway_ip=gateway,allocation_pools_start=allocation_pools_start,
                        allocation_pools_end=allocation_pools_end,enable_dhcp=enable_dhcp)
            n.save()
            return HttpResponseRedirect('/repo_home/')
    else:
        rf = AddNetworkForm()
    return render(request,'repo_create_network.html',{'rf':rf})



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
        save_path = "/home/mcy/upload/files/images"
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


def repo_handle_upload_image(f):
    pass



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




#----test----------------
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    with open('/home/mcy/upload/files/file_name.txt','wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
#--------------------------




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
    gname = forms.CharField(label='Gname',max_length=50,
                            error_messages={'required': 'The username can not be null!','max_length':'The group name is too long'},validators=[validate_gname])
    desc = forms.CharField(label='Gdesc',max_length=500,
                           widget=forms.Textarea(),
                           required=False,
                           initial="Replace with your feedbace",
                           error_messages={'max_length':'The description is too long'})
    stulist = forms.MultipleChoiceField(label='Stulist',required=False,
                                        widget=forms.CheckboxSelectMultiple,
                                        # choices=STU_CHECKBOX_CHOICES,
                                        )

    def __init__(self, *args, **kwargs):
        super(AddGroupForm, self).__init__(*args, **kwargs)
        # t= self.get_currentuser(request)
        self.fields['stulist'].choices = [(i.pk, str(i)) for i in Student.objects.all()]


def group_create(request):
    #get input from UI-----------------------UI---------------------------------
    username = request.session['username']
    if request.method == 'POST':
        rf = AddGroupForm(request.POST)
        if rf.is_valid():
            #get data from form
            gname = rf.cleaned_data['gname']
            desc = rf.cleaned_data['desc']
            stu_idlist = rf.cleaned_data['stulist']

            #insert into db
            gteacher = User.objects.get(username=username)
            stulist = []
            for i in range(0,len(stu_idlist)):
                stu = Student.objects.get(id=stu_idlist[i])
                stulist.append(stu)
            gcount = len(stu_idlist)

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
    try:
        g = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise Http404

    s_list = g.student.all()
    s_id_list = []
    for item in s_list:
        s_id_list.append(item.id)

    #edit and update the group
    username = request.session['username']
    if request.method == 'POST':
        rf = AddGroupForm(request.POST)
        if rf.is_valid():
            # get data from form
            update_gname = rf.cleaned_data['gname']
            update_desc = rf.cleaned_data['desc']
            update_stu_idlist = rf.cleaned_data['stulist']

            # edit basic info of group
            gteacher = User.objects.get(username=username)
            update_stulist = []
            for i in range(0, len(update_stu_idlist)):
                stu = Student.objects.get(id=update_stu_idlist[i])
                update_stulist.append(stu)
            update_gcount = len(update_stu_idlist)

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
        # initial the form
        attrs = {}
        attrs['gname'] = g.name
        attrs['desc'] = g.desc
        attrs['stulist'] = s_id_list
        gf = AddGroupForm(initial=attrs)
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


def router_list(request):
    pass


def server_list(request):
    # create conn to openstack
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    # define sth used to deliver to html
    ServerList = []
    ServerList = compute_resource_operation.list_servers(conn)

    return render(request, 'image_list.html', {'ServerList': ServerList})


#list all image
def image_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    ImageList = image_resource_operation.list_images(conn)
    context = {}
    context["ImageList"] = ImageList
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
    auth_username = 'teacher'
    auth_password = 'os62511279'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'teacher'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    image_id = 'c038649a-04e9-4603-8fc9-83a92d0f835e'
    image_resource_operation.delete_image(conn,image_id)
    return HttpResponse('Image delete Success!')



def network_delete(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    n_id = ''
    network_resource_operation.delete_network(conn,n_id)
    return HttpResponse('Network delete Success!')



def server_delete(request):
    # use local var
    auth_username = 'demo'
    auth_password = 'os62511279'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'demo'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    server_id = '386e7807-4aee-4f74-957f-f27b56b87be0'
    compute_resource_operation.delete_server(conn,server_id)
    return HttpResponse('VM delete Success' )


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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



def image_create(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    #Get the uploaded image file name
    image_name = upload_imageFile()#???????
    image_resource_operation.upload_image(conn,image_name)
    # List current image list
    ImageList = image_resource_operation.list_images(conn)

    c = {}
    c['ImageList']=ImageList
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
    n = network_resource_operation.create_network(conn,network_name,subnet_name,ip_version,cidr,gateway_ip)
    return HttpResponse('Create new network!')


def router_create(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    router_name = 'new-router'
    external_net_name = 'public'
    r = network_resource_operation.create_router(conn,router_name,external_net_name)
    return HttpResponse('Create new Router')

def gateway_add_to_router(request):
    pass

def interface_add_to_router(request):
    pass

def interface_delete_from_router(request):
    pass


def network_update(request):
    pass

def image_update(request):
    pass
#***********************************************************************#
#                          system exp  operate function         #
#***********************************************************************#
# def exp_list(request):
#     expList = experiment_operation.list_experiment()
#     c = Context({'expList':expList})
#     return render_to_response('image_list.html',c)


#only role = stu has this function
def exp_list_undo(request):
    username = request.session['username']
    student = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=student,situation='undo').order_by('-createTime')
    context={}
    context['ScoreList'] = ScoreList
    return render(request,'exp_list_undo.html',context)

def exp_list_doing(request):
    username = request.session['username']
    student = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=student,situation='doing').order_by('-createTime')
    context={}
    context['ScoreList'] = ScoreList
    return render(request,'exp_list_doing.html',context)

def exp_list_done(request):
    username = request.session['username']
    student = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=student,situation='done').order_by('-createTime')
    context={}
    context['ScoreList'] = ScoreList
    return render(request,'exp_list_done.html',context)

def exp_list_scored(request):
    username = request.session['username']
    student = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=student,situation='scored').order_by('-createTime')
    context={}
    context['ScoreList'] = ScoreList
    return render(request,'exp_list_scored.html',context)




#only role = teacher has this function
def exp_copy(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404

    imageList = e.exp_images.all()
    networkList = e.exp_network.all()
    images_idList=[]
    networks_idList=[]
    for item in imageList:
        images_idList.append(item.id)
    for item in networkList:
        networks_idList.append(item.id)
    # initial the form
    attrs = {}
    attrs['name'] = e.exp_name + "_copy"
    attrs['desc'] = e.exp_description
    attrs['images_idList'] = images_idList
    attrs['networks_idList'] = networks_idList
    attrs['guide'] = e.exp_guide
    attrs['refer_result'] = e.exp_result
    gf = AddExpForm(request, initial=attrs)

    #insert a new record into db
    username = request.session['username']
    t = User.objects.get(username=username)
    if request.method == 'POST':
        rf = EditExpForm(request.POST)
        if rf.is_valid():
            #get input data from form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            images_idList = rf.cleaned_data['images_idList']
            networks_idList = rf.cleaned_data['networks_idList']
            guide = rf.cleaned_data['guide']
            refer_result=rf.cleaned_data['refer_result']
            #get images
            imageList=[]
            for i in images_idList:
                imageList.append(VMImage.objects.get(id=i))
            networkList=[]
            for i in networks_idList:
                networkList.append(Network.objects.get(id=i))
            #get networks

            e = Experiment(exp_name=name,exp_description=desc,exp_owner=t,exp_image_count=len(imageList),
                           exp_guide=guide,exp_result=refer_result)
            e.save()
            for item in imageList:
                e.exp_images.add(item)
            for item in networkList:
                e.exp_network.add(item)

            #refresh the exp list
                return HttpResponseRedirect('/exp_home/')
    else:
        rf = EditExpForm()
    return render_to_response("exp_copy.html",{'rf':gf})



#only role = teacher has this function
def exp_create(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    print request.user
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

#only role=teacher
def exp_create_VM(request,exp_id):
    username = request.session['username']
    t = User.objects.get(username=username)
    if request.method == 'POST':
        rf = AddVMForm(request.POST)
        if rf.is_valid():
            #get data from form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            image_id = rf.cleaned_data['image_id']
            network_id = rf.cleaned_data['network_id']
            flavor = rf.cleaned_data['flavor']
            keypair = rf.cleaned_data['keypair']
            security_group = rf.cleaned_data['security_group']

            #get image
            image = VMImage.objects.get(id = image_id)
            #get networks
            net = Network.objects.get(id = network_id)
            #get experiment
            e = Experiment.objects.get(id=exp_id)
            #insert into VM
            vm = VM(name=name,desc=desc,owner=t,exp=e,image=image,network=net,flavor=flavor,keypair=keypair,security_group=security_group)
            vm.save()
            #update the VM_count of Experiment
            re = Experiment.objects.filter(id=exp_id).update(VM_count=e.VM_count+1)
            return HttpResponseRedirect('/exp_home/')
    else:
        rf = AddVMForm()
    return render_to_response("exp_create_VM.html",{'rf':rf})

def exp_delete_VM(request,exp_id):

    pass

#only role=teacher
def repo_VM_edit(request,vm_id):
    try:
        vm = VM.objects.get(id=vm_id)
    except VM.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        rf = EditVMForm(request.POST)
        if rf.is_valid():
            #get data from form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            image_id = rf.cleaned_data['image_id']
            network_id = rf.cleaned_data['network_id']
            flavor = rf.cleaned_data['flavor']
            keypair = rf.cleaned_data['keypair']
            security_group = rf.cleaned_data['security_group']

            #get image
            image = VMImage.objects.get(id = image_id)
            #get networks
            net = Network.objects.get(id = network_id)

            re = VM.objects.filter(id = vm_id).update(name=name,desc=desc,image=image,network=net,flavor=flavor,keypair=keypair,security_group=security_group)
            return HttpResponseRedirect('/repo_VM_list/')
    else:
        #initial the form
        attrs = {}
        attrs['name']=vm.name
        attrs['desc']=vm.desc
        attrs['exp']=vm.exp.exp_name
        attrs['image_id']=vm.image.id
        attrs['network_id']=vm.network.id
        attrs['flavor']=vm.flavor
        attrs['keypair']=vm.keypair
        attrs['security_group']=vm.security_group

        gf = EditVMForm(initial=attrs)
    return render_to_response("repo_VM_edit.html",{'rf':gf})

#only role = teacher has this function
def exp_edit(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    imageList = e.exp_images.all()
    networkList = e.exp_network.all()
    images_idList=[]
    networks_idList=[]
    for item in imageList:
        images_idList.append(item.id)
    for item in networkList:
        networks_idList.append(item.id)

    #edit and update the exp
    if request.method == 'POST':
        rf = EditExpForm(request.POST)
        #get input data from form
        update_name = rf.data['name']
        update_desc = rf.data['desc']
        update_images_idList = rf.data['images_idList']
        update_networks_idList = rf.data['networks_idList']
        update_guide = rf.data['guide']
        update_refer_result = rf.data['refer_result']

        update_imageList =[]
        update_networkList=[]
        for i in update_images_idList:
            update_imageList.append(VMImage.objects.get(id=i))
        for i in update_networks_idList:
            update_networkList.append(Network.objects.get(id=i))

        #update basic info for exp
        re = Experiment.objects.filter(id=exp_id).update(exp_name=update_name,exp_description=update_desc,
                                                         exp_image_count=len(update_imageList),exp_guide=update_guide,
                                                         exp_result=update_refer_result,exp_updatetime=datetime.datetime.now())
        update_e = Experiment.objects.get(id=exp_id)
        #update image list and network list for exp
        for i in range(0,len(update_imageList)):
            if update_imageList[i] not in imageList:
                update_e.exp_images.add(update_imageList[i])
        for j in range(0,len(imageList)):
            if imageList[j] not in update_imageList:
                update_e.exp_images.remove(imageList[j])

        for item in update_networkList:
            if item not in networkList:
                update_e.exp_network.add(item)
        for item in networkList:
            if item not in update_networkList:
                update_e.exp_network.remove(item)
        #refersh the exp list
        return HttpResponseRedirect('/exp_home/')
    else:
        # initial the form
        attrs = {}
        attrs['name'] = e.exp_name
        attrs['desc'] = e.exp_description
        attrs['images_idList'] = images_idList
        attrs['networks_idList'] = networks_idList
        attrs['guide'] = e.exp_guide
        attrs['refer_result'] = e.exp_result
        gf = EditExpForm(initial=attrs)
    return render_to_response("exp_edit.html",{'rf':gf})



#only role = teacher has this function
def exp_share(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    #update the is_shared field in Experiment db
    re = Experiment.objects.filter(id=exp_id).update(is_shared=True,shared_time=datetime.datetime.now())
    if re:
        messages.success(request,"Share exp success!")
    return HttpResponseRedirect('/exp_home/')


#only role = teacher has this function
def exp_delivery(request,exp_id):
    username = request.session['username']
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    teacher = User.objects.get(username=username)
    # clear the TempGroup
    TempGroup.objects.all().delete()
    # insert into TempGroup
    GList = Group.objects.filter(teacher=teacher)
    for item in GList:
        new = TempGroup(name=item.name, owner=teacher)
        new.save()

    if request.method == 'POST':
        rf = ExpDeliveryForm(request.POST)
        if rf.is_valid():
            # get data from the form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            group_idList = rf.cleaned_data['group']
            startDateTime = rf.cleaned_data['startDateTime']
            endDateTime = rf.cleaned_data['endDateTime']
            # prepare other required data

            delivery_time = datetime.datetime.now()

            glist = []
            for i in range(0, len(group_idList)):
                g = Group.objects.get(id=group_idList[i])
                glist.append(g)
            # insert into db:delivery
            for j in range(0, len(glist)):
                stulist = glist[j].student.all()
                d = Delivery(name=name, desc=desc, delivery_time=delivery_time, teacher=teacher,
                             start_time=startDateTime, stop_time=endDateTime,
                             exp=e, group=glist[j], total_stu=len(stulist))
                d.save()
                #send email to inform stu
                stu_emailList = []
                for item in stulist:
                    stu_emailList.append(item.stu_email)
                email_subject = "Here is an Experiment to do!"
                message = "Hello, "+ username +" has deliveried an experiment:"+e.exp_name+"to you."
                send_mail(email_subject, message, 'machenyi2011@163.com', stu_emailList,fail_silently=False)

            # insert into db:score
            d_List = Delivery.objects.filter(name=name, teacher=teacher)
            for i in range(0, len(d_List)):
                stulist = d_List[i].group.student.all()
                for j in range(0, len(stulist)):  # insert a record into score db for every stu
                    new_score = Score(exp=d_List[i].exp, stu=stulist[j], scorer=teacher, delivery_id=d_List[i].id)
                    new_score.save()
        return HttpResponseRedirect('/exp_home/')
    else:
        attrs = {}
        attrs['name'] = "delivery_" + e.exp_name + "_" + time.strftime('%Y-%m-%d %X', time.localtime())
        gf = ExpDeliveryForm(initial=attrs)

    return render_to_response("exp_delivery.html", {'rf': gf})



#only role = teacher has this function
def exp_delete(request,exp_id):
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
    c['username']=request.session['username']
    c['E_Detail_Dict'] = E_Detail_Dict
    return render(request, 'exp_detail.html', c)


#teacher
def exp_launch(request,exp_id):# in fact, it create ExpInstance
    username = request.session['username']
    role = request.session['role']

    t = User.objects.get(username=username)
    e = Experiment.objects.get(id=exp_id)
    #launch network

    #create router

    #launch VM

    #insert into ExpInstance db

    pass

#when stu launch and teacher check exp result, use this function
def exp_score_launch(request,socre_id):
    pass

def exp_score_delete(request,score_id):
    pass


def exp_network_launch(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username,auth_password)
    e_id = 1
    experiment_operation.luanch_exp_network(conn, e_id)
    return HttpResponse('launch exp network!')

def exp_vm_launch(request):
    pass

#teacher and student both have
def exp_instance_start(request,exp_i_id):
    pass

def exp_instance_pause(request,exp_i_id):
    pass

def exp_instance_unpause(request,exp_i_id):
    pass

def exp_instance_suspend(request,exp_i_id):
    pass

def exp_instance_resume(request,exp_i_id):
    pass

#teacher and student both have
def exp_instance_stop(request,exp_i_id):
    pass

def exp_instance_save(request,exp_i_id):
    pass




#only role=stu has this operation
def exp_submit(request,d_id):
    username = request.session['username']
    role = request.session['role']
    if role=="teacher":
        return HttpResponse("Teacher do not have this function")
    else:
        s = Student.objects.get(username=username)
        if request.method == 'POST':
            # get data from form
            reportFile = request.FILES.get("reportFile",None)
            if not reportFile:
                return HttpResponse("no file to choose")
            save_path = "/home/mcy/upload/files/report"
            destination = open(os.path.join(save_path, reportFile.name), 'wb+')
            for chunk in reportFile.chunks():
                destination.write.chunks()
            destination.close()
            file_path=save_path+'/'+reportFile.name

            rf = SubmitExpForm(request.POST)
            result = rf.data['result']

            #update Score db
            re = Score.objects.filter(stu=s,delivery_id=d_id).update(result=result,report_path=file_path)
            if re:
                messages.success(request,"Submit Exp Result Success!")
            return HttpResponseRedirect('/exp_home/')
        else:
            rf = SubmitExpForm()
    return render(request,"exp_submit.html",{'rf':rf})


#使用迭代器加载文件，实现大文件的下载
def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def exp_guide_download(reuqest,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    if e.exp_guide_path:
        # 使用StreamingHttpResponse配合迭代器返回文件到页面
        response = StreamingHttpResponse(file_iterator(e.exp_guide_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(e.exp_guide_path)
        return response
    else:
        return HttpResponse("This exp does not have a guide file!")



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
#                  Teacher list resource in private repo                 #
#***********************************************************************#
#Models:VMImage(id,name,owner,is_public,created_time)



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