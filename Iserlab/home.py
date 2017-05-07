# -*- coding: UTF-8 -*-
#This page just include those data wanted to be show on home.html
import json
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
import os
import re

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


def clear_RouterInstance_db(request):
    result = RouterInstance.objects.all().delete()
    return HttpResponse("clear RouterInstance in db")


def clear_ExpInstance_db(request):
    result = ExpInstance.objects.all().delete()
    return HttpResponse("clear ExpInstance in db")


def clear_NetworkInstance_db(request):
    result = NetworkInstance.objects.all().delete()
    return HttpResponse("clear NetworkInstance in db")

def clear_VMInstance_db(request):
    result = VMInstance.objects.all().delete()
    return HttpResponse("clear VMInstance in db")

def clear_Scores_db(request):
    Score.objects.all().delete()
    return HttpResponse("clear Scores in db")
#----------------------


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
        ExpList = Experiment.objects.filter(exp_owner_name=username).order_by('-exp_createtime')
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
    print d.start_time
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

#mcy and qinli try on 2017-4-24 with ModleForm
# def delivery_create(request):
#     username = request.session['username']
#     teacher = User.objects.get(username=username)
#     if request.method =='POST':
#         rf = AddDeliveryForm(request.POST)
#         print "####"
#         if rf.is_valid():
#             print "******"
#             #get data from the form
#             name = rf.cleaned_data['name']
#             desc = rf.cleaned_data['desc']
#             elist = rf.cleaned_data['exp']
#             glist = rf.cleaned_data['group']
#             startDateTime = rf.cleaned_data['startDateTime']
#             endDateTime = rf.cleaned_data['endDateTime']
#             #prepare other required data
#
#             delivery_time = datetime.datetime.now()
#
#             expList =[]
#             for item in elist:
#                 expList.append(Experiment.objects.get(exp_name=item.exp_name))
#             groupList = []
#             for item in glist:
#                 groupList.append((Group.objects.get(name=item.name)))
#
#             # insert into db:delivery
#             for i in range(0,len(expList)):
#                 for j in range(0,len(groupList)):
#                     stulist = groupList[j].student.all()
#                     d = Delivery(name=name,desc=desc,delivery_time=delivery_time,teacher=teacher,
#                                  start_time=startDateTime,stop_time=endDateTime,
#                                  exp=expList[i],group=groupList[j],total_stu=len(stulist))
#                     d.save()
#             #insert into db:score
#             d_List = Delivery.objects.filter(name=name,teacher=teacher)
#             for i in range(0,len(d_List)):
#                 stulist = d_List[i].group.student.all()
#                 for j in range(0,len(stulist)):#insert a record into score db for every stu
#                     new_score = Score(exp=d_List[i].exp,stu=stulist[j],scorer= teacher,delivery_id=d_List[i].id)
#                     print new_score
#                     new_score.save()
#         return HttpResponseRedirect('/delivery_list/')
#     else:
#         rf = AddDeliveryForm()
#         rf.base_fields['exp'].queryset = Experiment.objects.filter(exp_owner_name=username)
#         rf.base_fields['group'].queryset = Group.objects.filter(teacher = teacher)
#     return render_to_response("delivery_create.html",{'rf':rf})




def delivery_create(request): # by mcy using MyTempExp and MyTempGroup 2017-4-25
    username = request.session['username']
    teacher = User.objects.get(username=username)

    if request.method =='POST':
        rf = AddDeliveryForm(request.POST)
        if rf.is_valid():
            print "**************************************************enter valid***********************************"
            #get data from the form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            e_idlist = rf.cleaned_data['exp']#this is MyTempExp id
            g_idlist = rf.cleaned_data['group']#this is MyTempGroup id
            startDateTime = rf.cleaned_data['startDateTime']
            endDateTime = rf.cleaned_data['endDateTime']
            #prepare other required data

            delivery_time = datetime.datetime.now()

            expList =[]#should be actual Exp in Experiment
            for i in e_idlist:
                temp_exp = MyTempExp.objects.get(id=i)
                expList.append(Experiment.objects.get(id=temp_exp.exp.id))
            groupList = []#should be actual Group in Group
            for i in g_idlist:
                temp_group = MyTempGroup.objects.get(id=i)
                groupList.append(Group.objects.get(id=temp_group.group.id))

            # insert into db:delivery
            for i in range(0,len(expList)):
                for j in range(0,len(groupList)):
                    stulist = groupList[j].student.all()
                    d = Delivery(name=name,desc=desc,delivery_time=delivery_time,teacher=teacher,
                                 start_time=startDateTime,stop_time=endDateTime,
                                 exp=expList[i],group=groupList[j],total_stu=len(stulist))
                    d.save()
            #insert into db:score
            d_List = Delivery.objects.filter(name=name,teacher=teacher)
            for i in range(0,len(d_List)):
                stulist = d_List[i].group.student.all()
                for j in range(0,len(stulist)):#insert a record into score db for every stu
                    new_score = Score(exp=d_List[i].exp,stu=stulist[j],scorer= teacher,delivery_id=d_List[i].id)
                    new_score.save()
        return HttpResponseRedirect('/delivery_list/')
    else:
        # # clear the MyTempExp
        # MyTempExp.objects.all().delete()
        # insert into MyTempExp
        EList = Experiment.objects.filter(exp_owner_name=username)
        for item in EList:#first check if already exist, if not exist, insert into!
            MyTempExp.objects.get_or_create(teacher=teacher, exp=item)
            # new = MyTempExp(teacher=teacher, exp=item)
            # new.save()
        # # clear the MyTempGroup
        # MyTempGroup.objects.all().delete()
        # insert into MyTempGroup
        GList = Group.objects.filter(teacher=teacher)
        for item in GList:
            MyTempGroup.objects.get_or_create(teacher=teacher, group=item)
            # new = MyTempGroup(teacher=teacher, group=item)
            # new.save()
        rf = AddDeliveryForm()
    return render_to_response("delivery_create.html",{'rf':rf})


# #mcy and qinli try on 2017-3-19
# def delivery_create(request):
#     username = request.session['username']
#     teacher = User.objects.get(username=username)
#     # eQuerySet = Experiment.objects.filter(exp_owner_name=username)
#     # gQuerySet = Group.objects.filter(teacher=teacher)
#
#     # # clear the MyTempExp
#     # MyTempExp.objects.all().delete()
#     # #insert into MyTempExp
#     # EList= Experiment.objects.filter(exp_owner_name=username)
#     # for item in EList:
#     #     new = MyTempExp(teacher=teacher,exp=item)
#     #     new.save()
#     #
#     #
#     # #clear the TempGroup
#     # TempGroup.objects.all().delete()
#     # #insert into TempGroup
#     # GList=Group.objects.filter(teacher=teacher)
#     # for item in GList:
#     #     new = TempGroup(name=item.name, desc=item.desc, teacher=item.teacher, stuCount=item.stuCount)
#     #     new.save()
#
#     if request.method =='POST':
#         rf = AddDeliveryForm(request.POST)
#         print "####"
#         if rf.is_valid():
#             print "******"
#             #get data from the form
#             name = rf.cleaned_data['name']
#             desc = rf.cleaned_data['desc']
#             elist = rf.cleaned_data['exp']
#             glist = rf.cleaned_data['group']
#             startDateTime = rf.cleaned_data['startDateTime']
#             endDateTime = rf.cleaned_data['endDateTime']
#             #prepare other required data
#
#             delivery_time = datetime.datetime.now()
#
#             expList =[]
#             for item in elist:
#                 expList.append(Experiment.objects.get(exp_name=item.exp_name))
#             groupList = []
#             for item in glist:
#                 groupList.append((Group.objects.get(name=item.name)))
#
#             # insert into db:delivery
#             for i in range(0,len(expList)):
#                 for j in range(0,len(groupList)):
#                     stulist = groupList[j].student.all()
#                     d = Delivery(name=name,desc=desc,delivery_time=delivery_time,teacher=teacher,
#                                  start_time=startDateTime,stop_time=endDateTime,
#                                  exp=expList[i],group=groupList[j],total_stu=len(stulist))
#                     d.save()
#             #insert into db:score
#             d_List = Delivery.objects.filter(name=name,teacher=teacher)
#             for i in range(0,len(d_List)):
#                 stulist = d_List[i].group.student.all()
#                 for j in range(0,len(stulist)):#insert a record into score db for every stu
#                     new_score = Score(exp=d_List[i].exp,stu=stulist[j],scorer= teacher,delivery_id=d_List[i].id)
#                     print new_score
#                     new_score.save()
#         return HttpResponseRedirect('/delivery_list/')
#     else:
#         rf = AddDeliveryForm()
#     return render_to_response("delivery_create.html",{'rf':rf})




#pay attention to multi exps to multi group
# def delivery_create(request):
#     username = request.session['username']
#     teacher = User.objects.get(username=username)
#
#     #clear the MyTempExp
#     MyTempExp.objects.all().delete()
#     #insert into MyTempExp
#     EList= Experiment.objects.filter(exp_owner_name=username)
#     for item in EList:
#         new = MyTempExp(teacher=teacher,exp=item)
#         new.save()
#
#     #clear the TempGroup
#     TempGroup.objects.all().delete()
#     #insert into TempGroup
#     GList=Group.objects.filter(teacher=teacher)
#     for item in GList:
#         new = TempGroup(name=item.name,owner=teacher)
#         new.save()
#
#     if request.method =='POST':
#         rf = AddDeliveryForm(request.POST)
#         if rf.is_valid():
#             print "******"
#             #get data from the form
#             name = rf.cleaned_data['name']
#             desc = rf.cleaned_data['desc']
#             exp_idList = rf.cleaned_data['exp']
#             group_idList = rf.cleaned_data['group']
#             startDateTime = rf.cleaned_data['startDateTime']
#             endDateTime = rf.cleaned_data['endDateTime']
#             #prepare other required data
#
#             delivery_time = datetime.datetime.now()
#
#             elist = []
#             glist = []
#             for i in range(0,len(exp_idList)):
#                 e = Experiment.objects.get(id=exp_idList[i])
#                 elist.append(e)
#             for i in range(0,len(group_idList)):
#                 g = Group.objects.get(id = group_idList[i])
#                 glist.append(g)
#             # insert into db:delivery
#             for i in range(0,len(elist)):
#                 for j in range(0,len(glist)):
#                     stulist = glist[j].student.all()
#                     d = Delivery(name=name,desc=desc,delivery_time=delivery_time,teacher=teacher,
#                                  start_time=startDateTime,stop_time=endDateTime,
#                                  exp=elist[i],group=glist[j],total_stu=len(stulist))
#                     print d
#                     d.save()
#             #insert into db:score
#             d_List = Delivery.objects.filter(name=name,teacher=teacher)
#             for i in range(0,len(d_List)):
#                 stulist = d_List[i].group.student.all()
#                 for j in range(0,len(stulist)):#insert a record into score db for every stu
#                     new_score = Score(exp=d_List[i].exp,stu=stulist[j],scorer= teacher,delivery_id=d_List[i].id)
#                     print new_score
#                     new_score.save()
#         return HttpResponseRedirect('/delivery_list/')
#     else:
#         rf = AddDeliveryForm()
#     return render_to_response("delivery_create.html",{'rf':rf})


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
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    stu = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=stu,situation='Scored').order_by("-scoreTime")

    group_list=[]
    for item in ScoreList:
        g = Group.objects.get(id = item.group_id)
        if g not in group_list:
            group_list.append(g)

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



# 2017-03-28 qinli update
# def repo_image_delete(request,i_id):
#     try:
#         image = VMImage.objects.get(id=i_id)
#     except VMImage.DoesNotExist:
#         raise Http404
#     result = VMImage.objects.filter(id=i_id).delete()
#     #openstack API
#
#     if result:
#         print "delete success"
#     return HttpResponseRedirect('/repo_private_image_list/')


def repo_image_delete(request,i_id):
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404

    username = request.session['username']
    user_id = User.objects.get(username=username).id

    img = VMImage.objects.get(id=i_id)

    if img.owner_name == username:
        image_id = img.image_id #image_id存的是openstack中的image_id
        conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)

        #删除OpenStack中的镜像
        image_resource_operation.delete_image(conn, image_id)

        #删除数据库中记录
        img.delete()
        print "delete success"

    return HttpResponseRedirect('/repo_private_image_list/')
#end 2017-03-28 qinli update


# 2017-03-28 qinli update

def repo_image_share(request,i_id):
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404
    re = VMImage.objects.filter(id=i_id).update(is_shared=True)
    if re:
        print "repo_image_share Success!"
    return HttpResponseRedirect('/repo_private_image_list/')


def repo_image_share1(request,i_id):
    try:
        image = VMImage.objects.get(id=i_id)
    except VMImage.DoesNotExist:
        raise Http404

    username = request.session['username']
    user_id = User.objects.get(username=username).id

    if VMImage.objects.filter(id=i_id):
        image = VMImage.objects.get(id=i_id)
        if image.is_shared == 'True':
            image.is_shared = 'False'
            image.save()
            print 'image ' + i_id + ' is now private'
            return HttpResponseRedirect('/repo_private_image_list/')
        if image.is_shared == 'False':
            image.is_shared = 'True'
            image.save()
            print 'image ' + i_id + ' is now shared'
            return HttpResponseRedirect('/repo_private_image_list/')
    return HttpResponseRedirect('/repo_private_image_list/')
#end 2017-03-28 qinli update


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
            print "*******"
            # get data from form input
            name = rf.cleaned_data['name']
            subnet_name = rf.cleaned_data['subnet_name']
            desc = rf.cleaned_data['desc']
            ip_version = rf.cleaned_data['ip_version']
            cidr = rf.cleaned_data['cidr']
            gateway = rf.cleaned_data['gateway']
            # allocation_pools_start = rf.cleaned_data['allocation_pools_start']
            # allocation_pools_end = rf.cleaned_data['allocation_pools_end']
            enable_dhcp = rf.cleaned_data['enable_dhcp']
            #update the data in db
            re = Network.objects.filter(id=n_id).update(network_name=name,network_description=desc,subnet_name=subnet_name,
                                                        ip_version=ip_version,cidr=cidr,gateway_ip=gateway,
                                                        # allocation_pools_start=allocation_pools_start,
                                                        # allocation_pools_end=allocation_pools_end,
                                                        enable_dhcp=enable_dhcp,
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
#
def repo_VM_edit(request,vm_id):
    try:
        vm = VM.objects.get(id=vm_id)
    except VM.DoesNotExist:
        raise Http404

    username = request.session['username']
    teacher = User.objects.get(username=username)

    if request.method == 'POST':
        print "POST"
        rf = EditVMForm(request.POST)
        print "rf"
        # if rf.is_valid():
        print "########"
        #get data from form
        update_name = rf.data['name']
        update_desc = rf.data['desc']
        update_image_id = rf.data['image_id']#this id is MyTempImage id
        update_network_id = rf.data['network_id']#this id is MyTempNetwork id
        flavor = rf.data['flavor']
        keypair = rf.data['keypair']
        security_group = rf.data['security_group']

        image_in_cart = ImageCart.objects.get(id=update_image_id)
        image = VMImage.objects.get(id = image_in_cart.image.id)
        net_in_cart = NetworkCart.objects.get(id=update_network_id)
        net = Network.objects.get(id=net_in_cart.network.id)
        re = VM.objects.filter(id=vm_id).update(name=update_name,desc=update_desc,image=image,network=net,
                                                        flavor=flavor,keypair=keypair,security_group=security_group
                                                        )
        return HttpResponseRedirect('/repo_private_VM_list/')
    else:
        # prepare allimages that can be accessed by current user
        imageList = VMImage.objects.filter(owner_name=username)
        for item in imageList:
            MyTempImage.objects.get_or_create(teacher=teacher,image=item)
        imageList2 = VMImage.objects.filter(is_shared=True)
        imageList2 = imageList2.exclude(owner_name=username)
        for item in imageList2:
            MyTempImage.objects.get_or_create(teacher=teacher,image=item)

        netList = Network.objects.filter(owner_name=username)
        for item in netList:
            MyTempNetwork.objects.get_or_create(teacher=teacher,network=item)
        netList2 = Network.objects.filter(is_shared=True)
        netList2 = netList2.exclude(owner_name=username)
        for item in netList2:
            MyTempNetwork.objects.get_or_create(teacher=teacher,network=item)


        image_in_temp=MyTempImage.objects.get(image=vm.image)
        net_in_temp=MyTempNetwork.objects.get(network=vm.network)
        attrs = {}
        attrs['name']=vm.name
        attrs['desc']=vm.desc
        attrs['exp']=vm.exp
        attrs['image_id']= image_in_temp.id#this should be MyTempImage id
        attrs['network_id'] = net_in_temp.id#this thoudl be MyTempNetwork id
        attrs['flavor'] = vm.flavor
        attrs['keypair'] = vm.keypair
        attrs['security_group']="default"
        gf = EditVMForm(initial=attrs)
    return render_to_response("repo_VM_edit.html",{'rf':gf})


def repo_VM_delete(request,vm_id):
    try:
        vm = VM.objects.get(id=vm_id)
    except VM.DoesNotExist:
        raise Http404
    # update the vm_count field in Experiment db
    vm = VM.objects.get(id=vm_id)
    #first check whether the vm is belong to an Experiment
    if vm.exp:
        Experiment.objects.filter(id=vm.exp.id).update(VM_count=vm.exp.VM_count-1)

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
    PrivateExpList = Experiment.objects.filter(exp_owner_name=username).order_by('-exp_createtime')
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
    PrivateImageList = VMImage.objects.filter(owner_name=username).order_by('-created_at')
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
    NetList = Network.objects.filter(owner_name=username).order_by('-created_at')
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
    VMList = VM.objects.filter(owner_name=username).order_by('-created_at')
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
            n = Network(owner_name=username,network_name=name,network_description=desc,subnet_name=subnet_name,ip_version=ip_version,
                        cidr=cidr,gateway_ip=gateway,allocation_pools_start=allocation_pools_start,
                        allocation_pools_end=allocation_pools_end,enable_dhcp=enable_dhcp)
            n.save()
            return HttpResponseRedirect('/repo_home/')
    else:
        rf = AddNetworkForm()
    return render(request,'repo_create_network.html',{'rf':rf})



def repo_create_vm(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    if request.method == 'POST':
        rf = AddVMForm(request.POST)
        if rf.is_valid():
            # get data from form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            image_id = rf.cleaned_data['image_id']#this is imagecart id
            network_id = rf.cleaned_data['network_id']#this is netcart id
            flavor = rf.cleaned_data['flavor']
            keypair = rf.cleaned_data['keypair']
            security_group = rf.cleaned_data['security_group']

            # get image
            image_in_cart = ImageCart.objects.get(id=image_id)
            image = VMImage.objects.get(id=image_in_cart.image.id)
            # get networks
            net_in_cart = NetworkCart.objects.get(id=network_id)
            net = Network.objects.get(id=net_in_cart.network.id)

            # insert into VM
            vm = VM(name=name, desc=desc, owner_name=username, image=image, network=net, flavor=flavor,
                    keypair=keypair, security_group=security_group)
            vm.save()

            return HttpResponseRedirect('/repo_private_VM_list/')
    else:
        rf = AddVMForm()
    return render_to_response("repo_create_vm.html", {'rf': rf})


# 2017-03-28 qinli update
# def repo_create_image(request):
#     username = request.session['username']
#     t = User.objects.get(username=username)
#     # if request.method == 'POST':
#     #     form = CreateImageForm(request.POST,request.FILES)
#     #     if form.is_valid():
#     #         repo_handle_upload_image()
#     # pass
#     if request.method =="POST":
#         myfile = request.FILES.get("myfile",None)
#         if not myfile:
#             return HttpResponse("no file to choose")
#         save_path = "/home/mcy/upload/files/images"
#         destination = open(os.path.join(save_path,myfile.name),'wb+')
#         for chunk in myfile.chunks():
#             destination.write(chunk)
#         destination.close()
#
#         #get data from form
#         rf = CreateImageForm(request.POST)
#         name = rf.data['name']
#         desc = rf.data['desc']
#
#         #insert into db
#         file_path = save_path+'/'+myfile.name
#         new = VMImage(name=name,description=desc,path=file_path,owner_name=username)
#         new.save()
#
#         # response = "congrats. your file \"" + myfile.name + "\" has been uploaded."
#         return HttpResponseRedirect("/repo_home/")
#     else:
#         rf = CreateImageForm()
#     return render(request,'repo_create_image.html',{'rf':rf})

#上传文件

#验证输入的镜像名是否可用
def valid_name(name):
    if VMImage.objects.filter(name=name):
        return False
    return True


#上传镜像到服务器本地
def upload_image_file(image_file):
    save_path = "/home/mcy/upload/files/images"  # 文件存储的绝对路径
    destination = open(os.path.join(save_path, image_file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in image_file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    file_path = save_path + '/' + image_file.name
    return file_path

def repo_create_image(request):
    username = request.session['username']
    user_id = User.objects.get(username=username).id
    if request.method == "POST":  # 请求方法为POST时，进行处理
        # 取出表格中内容
        rf = upload_form(request.POST)
        image_name = rf.data['file_name']

        # 验证名字是否可用
        if not valid_name(image_name):
            return HttpResponse('the name is invalid!')

        # 上传镜像到服务器本地
        image_file = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not image_file:
            return HttpResponse("no files for upload!")
        file_path = upload_image_file(image_file)


        # 将镜像upload到OpenStack
        from image_resource_operation import upload_image
        from createconn_openstackSDK import create_connection

        with open(file_path) as imgfile:
            image_data = imgfile.read()

        conn = create_connection(auth_url, region_name, project_name, auth_username, auth_password)
        ret_image = upload_image(conn, image_name, image_data)

        # 将文件信息写入数据库
        new_image = VMImage()
        # new_image.image_id = conn.image.get_image(ret_image)

        # new_image.image_id = ret_image.id
        new_image.image_id = ret_image.id
        new_image.name = image_name
        # new_image.owner_id = user_id
        new_image.is_shared = 'False'
        new_image.owner_name = username
        new_image.own_project = 'True'
        new_image.size = 0
        # 其余Image信息补充
        # pass
        new_image.save()

        print 'Upload image!'
        return HttpResponseRedirect("/repo_home/")

    else:
        rf = upload_form()
    return render(request, 'repo_create_image.html', {'rf':rf})
#end 2017-03-28 qinli update


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


# 2017-03-28 qinli update
def repo_search(request):
    from forms import search_form
    if request.method == "POST":
        rf = search_form(request.POST)

        #当前用户名
        username = request.session['username']
        user_id = User.objects.get(username=username).id

        if rf.is_valid():
            id = rf.cleaned_data['id']
            name = rf.cleaned_data['name']
            owner = rf.cleaned_data['owner']

        #处理Image部分
            # 根据当前用户信息得到的其可见的Image
            private_ilist = list(VMImage.objects.filter(owner_id=user_id))
            shared_ilist = list(VMImage.objects.filter(is_shared='True'))
            #可见的Image为公有和私有的并集
            own_ilist = list(set(private_ilist) | set(shared_ilist))


            # id选项非空，则筛选出符合要求的Image，取交集
            if id:
                id_ilist = list(VMImage.objects.filter(image_id=id))
                own_ilist = list(set(own_ilist) & set(id_ilist))


            # name选项非空，则筛选出符合要求的Image，取交集
            if name:
                name_ilist = list(VMImage.objects.filter(name=name))
                own_ilist = list(set(own_ilist) & set(name_ilist))

            # owner选项非空，则筛选出符合要求的Image，取交集
            if owner:
                owner_ilist = list(VMImage.objects.filter(owner__username=owner))
                own_ilist = list(set(own_ilist) & set(owner_ilist))



        #处理Experiment部分
            # 根据当前用户信息得到的其可见的Experiment
            private_elist = list(Experiment.objects.filter(exp_owner_name=username))
            shared_elist = list(Experiment.objects.filter(is_shared='True'))
            # 可见的Image为公有和私有的并集
            own_elist = list(set(private_elist) | set(shared_elist))


            # name选项非空，则筛选出符合要求的Experiment，取交集
            if name:
                name_elist = list(Experiment.objects.filter(exp_name=name))
                own_elist = list(set(own_elist) & set(name_elist))

            # owner选项非空，则筛选出符合要求的Experiment，取交集
            if owner:
                owner_elist = list(Experiment.objects.filter(exp_owner__username=owner))
                own_elist = list(set(own_elist) & set(owner_elist))

            own_list = []
            own_list.append(own_ilist)
            own_list.append(own_elist)

            return render(request, 'search_result_ql.html', {'list': own_list})

        else:
            return HttpResponse('invalid input')

    else:
        rf = search_form()
    return render(request, 'search_ql.html', {'rf': rf})
#end 2017-03-28 qinli update



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
    c['role'] = request.session['role']
    c['username'] = request.session['username']
    c['hello'] = 'welcome to our platfowm'
    c['currentTime'] = showTime.formatTime2()
    c['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())
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
            print stu_idlist
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
    for flavor in flavors:
        #extract flavor info to a dict
        FlavorList.append(flavor)
    # the type of the list object :< class 'openstack.compute.v2.flavor.FlavorDetail'>

    c = Context({'FlavorList': FlavorList})
    return render(request, 'image_list.html', c)

def network_subnet_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    NetworkList = network_resource_operation.list_networks2(conn)
    return render(request, 'image_list.html', {'NetworkList': NetworkList})

def network_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    NetworkList = network_resource_operation.list_networks(conn)
    return render(request, 'image_list.html', {'NetworkList': NetworkList})



def subnet_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    SubnetList = network_resource_operation.list_subnets(conn)
    return render(request,'image_list.html',{'SubnetList':SubnetList})


#Function : Initialize the Router info in RouterInstance
def router_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    routers = network_resource_operation.list_routers(conn)

    for item in routers:
        # get usefull info from APi returned data
        status = item['status']
        gateway_net_id = item['external_gateway_info']['network_id']
        gateway_subnet_id = item['external_gateway_info']['external_fixed_ips'][0]['subnet_id']
        gateway_ip_address = item['external_gateway_info']['external_fixed_ips'][0]['ip_address']
        name = item['name']
        routerIntance_id = item['id']
        tenant_id = item['tenant_id']

        project = identity_resource_operation.find_project(conn,item['tenant_id'])
        owner_username = project['name']

        #insert into RouterIntance db-----first check if already exist,if not then insert, to avoid repeat
        RouterInstance.objects.get_or_create(owner_username = owner_username,routerIntance_id = routerIntance_id,name = name,status = status,
                             gateway_net_id = gateway_net_id,gateway_subnet_id = gateway_subnet_id,
                             gateway_ip_address = gateway_ip_address,tenant_id = tenant_id)

    return render(request,'image_list.html',{'RouterList':routers})


def port_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    PortList = network_resource_operation.list_ports(conn)
    return render(request, 'image_list.html', {'PortList': PortList})

def port_get(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    port_id = '73da2c08-98d7-4505-9432-133424949e22'
    portDict = network_resource_operation.get_port(conn,port_id)
    PortList = []
    PortList.append(portDict)
    return render(request,'image_list.html', {'PortList': PortList})

def security_group_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    SGList = network_resource_operation.list_security_groups(conn)
    return render(request,'image_list.html',{'SGList':SGList})


def security_group_rules_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    SGRList = network_resource_operation.list_security_group_rules(conn)
    return render(request, 'image_list.html', {'SGRList': SGRList})


def server_list(request):
    # create conn to openstack
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    # define sth used to deliver to html
    ServerList = []
    ServerList = compute_resource_operation.list_servers(conn)
    return render(request, 'image_list.html', {'ServerList': ServerList})

def server_stop(request):
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)

    # conn to openstack API
    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                     authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])
    server_id="7b36737a-eecc-445c-8deb-6b07bc8a67fe"
    compute_resource_operation.start_server(conn,server_id)
    return HttpResponse("stop a server")


def server_snapshot(request):
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)

    # conn to openstack API
    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                     authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])
    server_id="17bb442b-3eec-4f5d-8871-e8bc4cd59c0b"
    name="111-snapshot-1"
    compute_resource_operation.create_server_image(conn,server_id,name)
    return HttpResponse("snapshot a server")


#list all image----we use this function
def image_list(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)#use admin
    ImageList = image_resource_operation.list_images(conn)

    for item in ImageList:
        project = identity_resource_operation.find_project(conn, item['owner_id'])
        owner_name = project['name']

        # if owner_name =='admin':
        #get useful info from API returned data
        image_id = item['id']
        name = item['name']

        own_project = item['owner_id']
        is_public = item['visibility']
        description = 'Please input description for the VMImage.'
        status = item['status']
        created_at = item['created_at']
        updated_at = item['updated_at']
        size = item['size']
        min_disk = item['min_disk']
        min_ram = item['min_ram']

        if is_public == "public":
            is_shared = True
            shared_time = datetime.datetime.now()
        else:
            is_shared = False

        disk_format = item['disk_format']

        # insert into VMImage db first check if already exist
        VMImage.objects.get_or_create(image_id = image_id,name=name,owner_name=owner_name,own_project=own_project,is_public=is_public,description=description,
                                      status=status,size=size,min_disk=min_disk,min_ram=min_ram,is_shared=is_shared,disk_format=disk_format)
        # else:
        #     print "not admin upload images"

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

def router_delete(request):
    auth_username = 'qinli'
    auth_password = '123456'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'qinli'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    router_id = 'c7fa5738-30b4-4bf1-8c8a-0aed1440e6a2'
    network_resource_operation.delete_router(conn,router_id)
    return HttpResponse('Router Delete Success')


def port_delete(request):
    pass


def router_get(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    router_id = '3f597b1f-f34c-41e7-bd1e-81321371545f'
    router_dict = network_resource_operation.get_router(conn,router_id)
    context ={}
    context['RouterDict']=router_dict
    return render(request,'image_list.html',context)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def server_create(request):
    #use local var
    auth_username = 'demo'
    auth_password = 'os62511279'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'demo'
    region_name = 'RegionOne'

    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)

    server_name = 'demo-111-cirros2'
    image_name ='cirros'
    flavor_name = 'm1.tiny'
    network_name = 'private_alice'
    private_keypair_name = 'mykey'
    print 'before into ******'
    server_dict = compute_resource_operation.create_server2(conn, server_name, image_name, flavor_name, network_name,private_keypair_name)
    print server_dict['id']
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
    auth_username = 'qinli'
    auth_password = '123456'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'qinli'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)

    network_name = 'qinli-network222'
    subnet_name = 'qinli-subnet222'
    ip_version = '4'
    cidr = '10.0.10.0/24'
    gateway_ip = '10.0.10.1'
    description='test network'
    username = 'qinli'

    n = network_resource_operation.create_network(conn,network_name,subnet_name,ip_version,cidr,gateway_ip)
    return HttpResponse('Create new network!')


def router_create(request):
    auth_username = 'qinli'
    auth_password = '123456'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'qinli'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)

    r = RouterInstance.objects.filter(owner_username='qinli')
    if r:# the router already exists
        pass
    else:
        router_name = "qinli-router"
        router_dict = network_resource_operation.create_router(conn,router_name)
        print "here is router-------"
        print router_dict
        print router_dict['id']
        new_router = RouterInstance(owner_username='qinli',routerIntance_id=router_dict['id'],
                                    name=router_name,status=router_dict['status'],
                                    tenant_id=router_dict['tenant_id'])
        new_router.save()
    return HttpResponse('Create new Router')


def gateway_add_to_router(request):
    auth_username = 'qinli'
    auth_password = '123456'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'qinli'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    router_id='938e9eda-bc98-44f2-9f81-6b01d14369da'
    external_net_name = "public"
    external_net_id = '4e9b7eea-fcd3-4773-bcb4-711b44979b18'
    #---
    r = network_resource_operation.get_router(conn, router_id)

    router_dict2 = network_resource_operation.add_gateway_to_router(conn, r, external_net_id)
    print router_dict2
    return HttpResponse('Add gateway to Router')


def gateway_remove_from_router(request):
    auth_username = 'qinli'
    auth_password = '123456'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'qinli'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    router_id = "938e9eda-bc98-44f2-9f81-6b01d14369da"
    r = network_resource_operation.get_router(conn,router_id)
    router_dict = network_resource_operation.remove_gateway_from_router(conn,r)
    return HttpResponse('Remove gateway from Router')

def interface_add_to_router(request):
    auth_username = 'qinli'
    auth_password = '123456'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'qinli'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    router_id = "938e9eda-bc98-44f2-9f81-6b01d14369da"
    r = network_resource_operation.get_router(conn, router_id)
    subnet_id = "a2dc25d3-c7cf-4fbf-85d7-3aef8618b584"

    print "start add interface"
    router_dict = network_resource_operation.add_interface_to_router(conn, r, subnet_id)
    print router_dict
    return HttpResponse('add interface to Router')


def interface_delete_from_router(request):
    pass

def port_create(request):
    pass

def port_delete(request):
    auth_username = 'qinli'
    auth_password = '123456'
    auth_url = 'http://202.112.113.220:5000/v2.0/'
    project_name = 'qinli'
    region_name = 'RegionOne'
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    port_id = ""
    network_resource_operation.delete_port(conn,port_id)
    return HttpResponse('delete port')

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
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    student = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=student,situation='undo').order_by('-createTime')
    context['ScoreList'] = ScoreList
    return render(request,'exp_list_undo.html',context)

def exp_list_doing(request):
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    student = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=student,situation='doing').order_by('-createTime')
    context['ScoreList'] = ScoreList
    return render(request,'exp_list_doing.html',context)

def exp_list_done(request):
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    student = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=student,situation='done').order_by('-createTime')
    context['ScoreList'] = ScoreList
    return render(request,'exp_list_done.html',context)

def exp_list_scored(request):
    context={}
    context['role']=request.session['role']
    context['username'] = request.session['username']
    context['hello']='welcome to our platfowm'
    context['currentTime']= showTime.formatTime2()
    context['currentTimeStamp']=showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    student = Student.objects.get(stu_username=username)
    ScoreList = Score.objects.filter(stu=student,situation='scored').order_by('-createTime')
    context['ScoreList'] = ScoreList
    return render(request,'exp_list_scored.html',context)




#only role = teacher has this function
def exp_copy(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404

    imageList = e.exp_images.all()#these are VMImage records
    networkList = e.exp_network.all()#these are Network records
    images_idList=[]#should be ImageCart id
    networks_idList=[]#should be NetworkCart id
    for item in imageList:
        image_in_cart = ImageCart.objects.get(image = item)
        images_idList.append(image_in_cart.id)
    for item in networkList:
        network_in_cart = NetworkCart.objects.get(network = item)
        networks_idList.append(network_in_cart.id)

    #insert a new record into db
    username = request.session['username']
    t = User.objects.get(username=username)
    if request.method == 'POST':
        rf = CopyExpForm(request.POST)
        if rf.is_valid():
            #get input data from form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            images_idList = rf.cleaned_data['images_idList']#this is ImageCart id
            networks_idList = rf.cleaned_data['networks_idList']#this is NetworkCart id

            #get images
            imageList=[]
            for i in images_idList:
                image_in_cart = ImageCart.objects.get(id =i)
                imageList.append(VMImage.objects.get(id=image_in_cart.image.id))
            #get networks
            networkList=[]
            for i in networks_idList:
                network_in_cart = NetworkCart.objects.get(id=i)
                networkList.append(Network.objects.get(id=network_in_cart.network.id))
            e = Experiment(exp_name=name,exp_description=desc,exp_owner_name=username,exp_image_count=len(imageList))
            e.save()
            for item in imageList:
                e.exp_images.add(item)
            for item in networkList:
                e.exp_network.add(item)

            #refresh the exp list
            return HttpResponseRedirect('/exp_home/')
    else:
        # initial the form
        attrs = {}
        attrs['name'] = e.exp_name + "_copy"
        attrs['desc'] = e.exp_description
        attrs['images_idList'] = images_idList#should be ImageCart id
        attrs['networks_idList'] = networks_idList#should be NetworkCart id
        attrs['vm_count']=e.VM_count
        gf = CopyExpForm(initial=attrs)

    return render_to_response("exp_copy.html",{'rf':gf})



#only role = teacher has this function
def exp_create(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    if request.method == 'POST':
        rf = AddExpForm(request.POST)
        if rf.is_valid():

            guideFile = request.FILES.get("guide_file",None)
            if not guideFile:
                return HttpResponse("no file to choose")
                # messages.error(request,"no file to choose")
            save_path = "/home/mcy/upload/files/guide"
            destination = open(os.path.join(save_path,guideFile.name),'wb+')
            for chunk in guideFile.chunks():
                destination.write(chunk)
            destination.close()
            #get input data from form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            images_idList = rf.cleaned_data['images_idList']#this id is ImageCart id
            networks_idList = rf.cleaned_data['networks_idList']#this id is NetworkCart id
            vm_count = rf.cleaned_data['vm_count']

            #get images
            imageList=[]
            for i in images_idList:
                image_in_cart = ImageCart.objects.get(id=i)
                imageList.append(VMImage.objects.get(id=image_in_cart.image.id))

            # get networks
            networkList=[]
            for i in networks_idList:
                network_in_cart = NetworkCart.objects.get(id=i)
                networkList.append(Network.objects.get(id=network_in_cart.network.id))


            exp_guide_path = save_path+'/'+guideFile.name
            e = Experiment(exp_name=name,exp_description=desc,exp_owner_name=username,exp_image_count=len(imageList),
                           exp_guide_path=exp_guide_path,VM_count=vm_count)
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
            image_id = rf.cleaned_data['image_id']#this is imagecart id
            network_id = rf.cleaned_data['network_id']#this is netcart id
            flavor = rf.cleaned_data['flavor']
            keypair = rf.cleaned_data['keypair']
            security_group = rf.cleaned_data['security_group']

            # get image
            image_in_cart = ImageCart.objects.get(id=image_id)
            image = VMImage.objects.get(id=image_in_cart.image.id)
            # get networks
            net_in_cart = NetworkCart.objects.get(id=network_id)
            net = Network.objects.get(id=net_in_cart.network.id)

            #get experiment
            e = Experiment.objects.get(id=exp_id)
            #insert into VM
            vm = VM(name=name,desc=desc,owner_name=username,exp=e,image=image,network=net,flavor=flavor,keypair=keypair,security_group=security_group)
            vm.save()
            #update the VM_count of Experiment
            re = Experiment.objects.filter(id=exp_id).update(VM_count=e.VM_count+1)
            return HttpResponseRedirect('/exp_home/')
    else:
        rf = AddVMForm()
    return render_to_response("exp_create_VM.html",{'rf':rf})

def exp_delete_VM(request,exp_id):
    username = request.session['username']
    t = User.objects.get(username=username)
    e = Experiment.objects.get(id=exp_id)
    vm_list = VM.objects.filter(exp=e,owner_name=username)
    vm_id_list = []
    for item in vm_list:
        vm_id_list.append(item.id)
    if len(vm_list):
        if request.method == 'POST':
            rf = DeleteVMForm(request.POST)
            if rf.is_valid():
                print "****"
                #get data from form
                delete_vm_id_list = rf.cleaned_data['vm_id_list']

                # update the VM_count of Experiment
                re = Experiment.objects.filter(id=exp_id).update(VM_count=e.VM_count - len(delete_vm_id_list))

                #delete from VM db
                for i in delete_vm_id_list:
                    VM.objects.filter(id=i).delete()
                return HttpResponseRedirect('/exp_home/')
        else:
            # rf = DeleteVMForm()
            attrs = {}
            attrs['exp_name'] = e.exp_name
            attrs['vm_id_list'] = vm_id_list
            gf = DeleteVMForm(initial=attrs)
        return render_to_response("exp_delete_VM.html",{'rf':gf})
    else:
        print "There is no vm to delete"
        return HttpResponse("No VM to delete!")


#only role = teacher has this function
def exp_edit(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    username = request.session['username']
    teacher = User.objects.get(username=username)

    #Refresh the MyTempImage db-------prepare all images that can be accessed by current user
    imageList = VMImage.objects.filter(owner_name=username)
    for item in imageList:
        MyTempImage.objects.get_or_create(teacher=teacher, image=item)
    imageList2 = VMImage.objects.filter(is_shared=True)
    imageList2 = imageList2.exclude(owner_name=username)
    for item in imageList2:
        MyTempImage.objects.get_or_create(teacher=teacher, image=item)

    #Refresh the MyTempNetwork db ------prepare all networks that can be accessed by current user
    netList = Network.objects.filter(owner_name=username)
    for item in netList:
        MyTempNetwork.objects.get_or_create(teacher=teacher,network = item)
    netList2 = Network.objects.filter(is_shared=True)
    netList2 = netList2.exclude(owner_name=username)
    for item in netList2:
        MyTempNetwork.objects.get_or_create(teacher=teacher,network = item)

    e_imageList = e.exp_images.all()
    e_networkList = e.exp_network.all()
    images_idList=[]#should be MyTempImage id
    networks_idList=[]#should be NetworkCart id
    for item in e_imageList:
        image_in_temp = MyTempImage.objects.get(image=item)
        images_idList.append(image_in_temp.id)
    for item in e_networkList:
        network_in_temp = MyTempNetwork.objects.get(network=item)
        networks_idList.append(network_in_temp.id)

    #edit and update the exp
    if request.method == 'POST':
        rf = EditExpForm(request.POST)
        if rf.is_valid():
            #get input data from form
            update_name = rf.cleaned_data['name']
            update_desc = rf.cleaned_data['desc']
            update_images_idList = rf.cleaned_data['images_idList']#this id is MyTempImage id
            update_networks_idList = rf.cleaned_data['networks_idList']#this id is MyTempNetwork id
            update_vm_count = rf.cleaned_data['vm_count']
            # update_guide = rf.data['guide']
            # update_refer_result = rf.data['refer_result']
            print "after update"
            print update_images_idList
            update_imageList =[]
            update_networkList=[]
            for i in update_images_idList:
                image_in_temp = MyTempImage.objects.get(id=i)
                update_imageList.append(VMImage.objects.get(id=image_in_temp.image.id))
            for i in update_networks_idList:
                network_in_temp = MyTempNetwork.objects.get(id=i)
                update_networkList.append(Network.objects.get(id=network_in_temp.network.id))

            #update basic info for exp
            re = Experiment.objects.filter(id=exp_id).update(exp_name=update_name,exp_description=update_desc,
                                                             exp_image_count=len(update_imageList),
                                                             exp_updatetime=datetime.datetime.now(),
                                                             VM_count=update_vm_count)
            update_e = Experiment.objects.get(id=exp_id)
            #update image list and network list for exp
            for i in range(0,len(update_imageList)):
                if update_imageList[i] not in e_imageList:
                    update_e.exp_images.add(update_imageList[i])
            for j in range(0,len(e_imageList)):
                if e_imageList[j] not in update_imageList:
                    update_e.exp_images.remove(e_imageList[j])

            for item in update_networkList:
                if item not in e_networkList:
                    update_e.exp_network.add(item)
            for item in e_networkList:
                if item not in update_networkList:
                    update_e.exp_network.remove(item)
            #refersh the exp list
            return HttpResponseRedirect('/exp_home/')
    else:
        # initial the form


        attrs = {}
        attrs['name'] = e.exp_name
        attrs['desc'] = e.exp_description
        attrs['images_idList'] = images_idList#this should be imagecart id
        attrs['networks_idList'] = networks_idList#this should be netcart id
        attrs['vm_count'] = e.VM_count
        gf = EditExpForm(initial=attrs)
    return render_to_response("exp_edit.html",{'rf':gf})


def image_share_function():
    return 0

#only role = teacher has this function
def exp_share(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    #update the is_shared field in Experiment db
    re = Experiment.objects.filter(id=exp_id).update(is_shared=True,shared_time=datetime.datetime.now())
    #also share the include images and net
    e_imageList = e.exp_images.all()
    e_networkList = e.exp_network.all()

    for image in e_imageList:
        vmimage = VMImage.objects.get(id=image.id)
        if vmimage.is_shared == False:
            vmimage.is_shared = True
            vmimage.shared_time = datetime.datetime.now()
            vmimage.save()
    for net in e_networkList:
        network = Network.objects.get(id=net.id)
        if network.is_shared == False:
            network.is_shared = True
            network.shared_time = datetime.datetime.now()
            network.save()
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

    if request.method == 'POST':
        rf = ExpDeliveryForm(request.POST)
        if rf.is_valid():
            print "**************************************************enter valid***********************************"
            # get data from the form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            group_idList = rf.cleaned_data['groups_idList']#this is MyTempGroup id
            startDateTime = rf.cleaned_data['startDateTime']
            endDateTime = rf.cleaned_data['endDateTime']
            # prepare other required data

            delivery_time = datetime.datetime.now()
            glist = []
            for i in group_idList:
                temp_group = MyTempGroup.objects.get(id =i)
                g = Group.objects.get(id=temp_group.group.id)
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
        # # clear the MyTempGroup
        # MyTempGroup.objects.all().delete()
        # insert into MyTempGroup
        GList = Group.objects.filter(teacher=teacher)
        for item in GList:# first check if exist,if not exist, insert.
            MyTempGroup.objects.get_or_create(teacher=teacher, group=item)
            # new = MyTempGroup(teacher=teacher, group=item)
            # new.save()
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

    username = request.session['username']
    role = request.session['role']
    #get exp detail info from db
    edict = {}
    ##edict={}.fromkeys('id','name','owner','imageCount','imagelist','network','is_shared','description')
    edict['id']=e.id
    edict['exp_name'] = e.exp_name
    edict['exp_owner_name'] = e.exp_owner_name
    edict['exp_createtime'] = e.exp_createtime
    edict['exp_updatetime'] = e.exp_updatetime
    edict['exp_image_count'] = e.exp_image_count
    imagelist = e.exp_images.all()
    edict['exp_images'] = imagelist
    network = e.exp_network.all()
    edict['exp_network'] = network
    edict['is_shared'] = e.is_shared
    edict['shared_time'] = e.shared_time
    edict['exp_description'] = e.exp_description
    edict['exp_guide_path'] = e.exp_guide_path
    edict['VM_count'] = e.VM_count
    VMList = VM.objects.filter(exp=e).order_by('-created_at')
    edict['VMList'] = VMList

    if role == 'teacher':
        teacher = User.objects.get(username=username)
        deliverys = Delivery.objects.filter(exp=e, teacher=teacher).order_by('-delivery_time')
        edict['delivery_history'] = deliverys
    # output the group detail-----------------------------UI--------------------------
    c = {}
    c['username']=username
    c['role']=role
    c['E_Detail_Dict'] = edict
    images = e.exp_images.all()
    vms = VM.objects.filter(exp=e)
    networks = e.exp_network.all()

    topo_ndict = {}
    count = 0
    topo_info = '{"nodes":['
    for vm in vms:
        count = count + 1
        topo_info = topo_info + '{"name":"' + vm.name + '","id":' + str(count) + ',"image":"Q-node"},'
        topo_ndict[vm.name] = count
    for network in networks:
        count = count + 1
        topo_info = topo_info + '{"name":"' + network.network_name + '","id":' + str(count) + ',"image":"Q-cloud"},'
        topo_ndict[network.network_name] = count
    count = count + 1
    topo_info = topo_info + '{"id":' + str(count) + ',"x":-100,"y":-50}], "edges": ['
    topo_ndict['router'] = count

    count = 0
    for vm in vms:
        count = count + 1
        if count != 1:
            topo_info = topo_info + ','
        topo_info = topo_info + '{"name":"","from":' + str(topo_ndict[vm.name]) + ',"to":' + str(
            topo_ndict[vm.network.network_name]) + '}'


    topo_info = topo_info + ']}'
    Topo = []
    Topo.append(topo_info)

    #  Topo=['{"nodes":[{"name": "C", "id": 3},{"name": "A", "x": -100, "y": -50, "id": 1}, {"name": "B", "id": 2}], "edges": [{"name": "Edge", "from":1, "to":2}]}']

    # ly topo 2017/4/6    return render(request, 'exp_detail.html',{'Topo':json.dumps(Topo),'c':c})
    return render(request, 'exp_detail.html', {'Topo': json.dumps(Topo), 'c': c})
    #return render(request, 'exp_detail.html', c)



#teacher
def exp_launch(request,exp_id):# in fact, it create ExpInstance
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username,u.password)
    else:
        u = Student.objects.get(stu_username = username)
        authDict = get_auth_info(u.stu_username,u.stu_password)

    # insert into ExpInstance db

    name = e.exp_name+'_instance'+username
    new_expInstance = ExpInstance(name= name,exp=e,owner_name=username)
    new_expInstance.save()
    print new_expInstance.id

    # conn to openstack API
    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                     authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])
    #launch network, insert into networkInstance
    nets = e.exp_network.all()
    router = RouterInstance.objects.get(owner_username=username)#admin already create a router for this user when register it
    for item in nets:
        new_net_instance = network_resource_operation.create_network(conn,item.network_name,item.subnet_name,
                                                                     item.ip_version,item.cidr,item.gateway_ip)
        print "here is network *******"
        print new_net_instance['id']
        new_net = NetworkInstance(name=item.network_name,owner_name=username,network=item,belong_exp_instance_id=new_expInstance.id,
                              network_instance_id=new_net_instance['id'],subnet_instance_id=new_net_instance['sub_id'],
                              tenant_id = new_net_instance['tenant_id'],status=new_net_instance['status'],
                              allocation_pools_start=new_net_instance['sub_allocation_pools'][0]['start'],
                              allocation_pools_end=new_net_instance['sub_allocation_pools'][0]['end'])
        new_net.save()

        #create interface to attach network to router
        r = network_resource_operation.add_interface_to_router(conn,router.routerIntance_id,new_net.subnet_instance_id)
    print "--------net create complete-------"

    # launch VM , insert into VMInstance
    vms = e.vm_set.all()  # 需要用foreignkey功能的话需要在VM的model中加入related_name
    for vm in vms:
        # launch VM ,
        server_name = vm.name
        image_name = vm.image.name
        flavor_name = vm.flavor
        network_name = vm.network.network_name  # should find the net instance
        private_keypair_name = vm.keypair

        # first check if the needed netInstance exist in NetworkInstance db?
        ni = NetworkInstance.objects.filter(owner_name=username, network=vm.network, status="ACTIVE")
        if len(ni) > 0:  # the Network Instance exist
            netInstance = NetworkInstance.objects.get(owner_name=username, network=vm.network, status="ACTIVE")
            vm_instance = compute_resource_operation.create_server2(conn, server_name, image_name, flavor_name,
                                                                    network_name, private_keypair_name)
            # insert into VMInstance db
            new_vmInstance = VMInstance(name=vm.name, owner_name=username, vm=vm,
                                        belong_exp_instance_id=new_expInstance.id,
                                        server_id=vm_instance['id'], status=vm_instance['status'],
                                        createtime=datetime.datetime.now(),
                                        updatetime=datetime.datetime.now(),
                                        connect_net=netInstance)
            new_vmInstance.save()
    #if both network and VMs create successfully, should update the status of ExpInstance
    re = ExpInstance.objects.filter(id=new_expInstance.id).update(instance_status="ACTIVE")
    return HttpResponseRedirect('/exp_instance_list/')


# if student, should update Score db
def exp_student_launch(request,s_id):# in fact, it create an ExpInstance
    try:
        s = Score.objects.get(id=s_id)
    except Score.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username,u.password)
    else:
        u = Student.objects.get(stu_username = username)
        authDict = get_auth_info(u.stu_username,u.stu_password)

    # insert into ExpInstance db
    e = s.exp
    name = e.exp_name+'_instance'+username
    new_expInstance = ExpInstance(name= name,exp=e,owner_name=username)
    new_expInstance.save()

    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                     authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])
    #launch network, insert into networkInstance
    nets = e.exp_network.all()
    router = RouterInstance.objects.get(owner_username=username)#admin already create a router for this user when register it
    for item in nets:
        new_net_instance = network_resource_operation.create_network(conn,item.network_name,item.subnet_name,
                                                                     item.ip_version,item.cidr,item.gateway_ip)

        print new_net_instance['id']
        new_net = NetworkInstance(name=item.network_name,owner_name=username,network=item,belong_exp_instance_id=new_expInstance.id,
                              network_instance_id=new_net_instance['id'],subnet_instance_id=new_net_instance['sub_id'],
                              tenant_id = new_net_instance['tenant_id'],status=new_net_instance['status'],
                              allocation_pools_start=new_net_instance['sub_allocation_pools'][0]['start'],
                              allocation_pools_end=new_net_instance['sub_allocation_pools'][0]['end'])
        new_net.save()

        #create interface to attach network to router
        r = network_resource_operation.add_interface_to_router(conn,router.routerIntance_id,new_net.subnet_instance_id)


    # launch VM , insert into VMInstance
    vms = e.vm_set.all()  # 需要用foreignkey功能的话需要在VM的model中加入related_name
    for vm in vms:
        # launch VM ,
        server_name = vm.name
        image_name = vm.image.name
        flavor_name = vm.flavor
        network_name = vm.network.network_name  # should find the net instance
        private_keypair_name = vm.keypair

        # first check if the needed netInstance exist in NetworkInstance db?
        ni = NetworkInstance.objects.filter(owner_name=username, network=vm.network, status="ACTIVE")
        if len(ni) > 0:  # the Network Instance exist
            netInstance = NetworkInstance.objects.get(owner_name=username, network=vm.network, status="ACTIVE")
            vm_instance = compute_resource_operation.create_server2(conn, server_name, image_name, flavor_name,
                                                                    network_name, private_keypair_name)
            # insert into VMInstance db
            new_vmInstance = VMInstance(name=vm.name, owner_name=username, vm=vm,
                                        belong_exp_instance_id=new_expInstance.id,
                                        server_id=vm_instance['id'], status=vm_instance['status'],
                                        createtime=datetime.datetime.now(),
                                        updatetime=datetime.datetime.now(),
                                        connect_net=netInstance)
            new_vmInstance.save()

    #if both network and VMs create successfully, should update the status of ExpInstance
    re = ExpInstance.objects.filter(id=new_expInstance.id).update(instance_status="ACTIVE",score_id=s_id)

    #also should update the Score db
    Score.objects.filter(id=s_id).update(situation='doing',exp_instance_id=new_expInstance.id,times=s.times+1,startTime=datetime.datetime.now())
    return HttpResponseRedirect('/exp_instance_list/')


#function: launch an instance from a exp template
#Input: exp template
#Output: exp Instance
def exp_launch_function(conn,e,username,role,s_id):
    # insert into ExpInstance db
    name = e.exp_name + '_instance' + username
    new_expInstance = ExpInstance(name=name, exp=e, owner_name=username)
    new_expInstance.save()

    # launch network, insert into networkInstance
    nets = e.exp_network.all()
    router = RouterInstance.objects.get(owner_username=username)  # admin already create a router for this user when register it
    for item in nets:
        new_net_instance = network_resource_operation.create_network(conn, item.network_name, item.subnet_name,
                                                                     item.ip_version, item.cidr, item.gateway_ip)

        new_netInstance = NetworkInstance(name=item.network_name, owner_name=username, network=item,
                                  belong_exp_instance_id=new_expInstance.id,
                                  network_instance_id=new_net_instance['id'],
                                  subnet_instance_id=new_net_instance['sub_id'],
                                  tenant_id=new_net_instance['tenant_id'], status=new_net_instance['status'],
                                  allocation_pools_start=new_net_instance['sub_allocation_pools'][0]['start'],
                                  allocation_pools_end=new_net_instance['sub_allocation_pools'][0]['end'])
        new_netInstance.save()

        # create interface to attach network to router
        r = network_resource_operation.add_interface_to_router(conn, router.routerIntance_id,new_netInstance.subnet_instance_id)

    # launch VM , insert into VMInstance
    vms = e.vm_set.all()  # 需要用foreignkey功能的话需要在VM的model中加入related_name
    for vm in vms:
        # launch VM ,
        server_name = vm.name
        image_name = vm.image.name
        flavor_name = vm.flavor
        network_name = vm.network.network_name  # should find the net instance
        private_keypair_name = vm.keypair

        # first check if the needed netInstance exist in NetworkInstance db?
        ni = NetworkInstance.objects.filter(owner_name=username, network=vm.network, status="ACTIVE")
        if len(ni) > 0:  # the Network Instance exist
            netInstance = NetworkInstance.objects.get(owner_name=username, network=vm.network, status="ACTIVE")
            vm_instance = compute_resource_operation.create_server2(conn, server_name, image_name, flavor_name,
                                                                    network_name, private_keypair_name)
            # insert into VMInstance db
            new_vmInstance = VMInstance(name=vm.name, owner_name=username, vm=vm,
                                        belong_exp_instance_id=new_expInstance.id,
                                        server_id=vm_instance['id'], status=vm_instance['status'],
                                        createtime=datetime.datetime.now(),
                                        updatetime=datetime.datetime.now(),
                                        connect_net=netInstance)
            new_vmInstance.save()

    # if both network and VMs create successfully, should update the status of ExpInstance
    if role == "teacher":
        re = ExpInstance.objects.filter(id=new_expInstance.id).update(instance_status="ACTIVE")
    else:
        re = ExpInstance.objects.filter(id=new_expInstance.id).update(instance_status="ACTIVE", score_id=s_id)
    return new_expInstance.id


#both teacher and student have this function
#Function : Launch the result_exp template of Score to check the experiment result
#Input: score_id
#Output: result exp instance
def exp_result_launch(request,s_id):
    username = request.session['username']
    role = request.session['role']
    if if_exp_instance_exist_function(username):
        return HttpResponse("There is already an exp Instance running, please save it as template first!")
    else:
        try:
            s = Score.objects.get(id=s_id)
        except Score.DoesNotExist:
            raise Http404

        if role == 'teacher':
            u = User.objects.get(username=username)
            authDict = get_auth_info(u.username,u.password)
        else:
            u = Student.objects.get(stu_username = username)
            authDict = get_auth_info(u.stu_username,u.stu_password)
        conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                         authDict['project_name'],
                                                         authDict['auth_username'], authDict['auth_password'])

        #get the result exp
        try:
            exp = Experiment.objects.get(id=s.result_exp_id)
        except Experiment.DoesNotExist:
            raise Http404
        print "the result exp id is:"
        print exp.id

        # use function to launch the exp instance
        new_ei_id = exp_launch_function(conn, exp, username, role, s_id)
        print "the launch result exp instance is:"
        print new_ei_id

        return HttpResponseRedirect('/exp_instance_list/')



def if_exp_instance_exist_function(username):
    eiList = ExpInstance.objects.filter(owner_name = username)
    eiList = eiList.exclude(instance_status="DELETED")
    if eiList:
        return True
    else:
        return False




#when stu launch and teacher check exp result, use this function-----not finished
def exp_score_launch1(request,score_id):
    try:
        score = Score.objects.get(id=score_id)
    except Score.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username,u.password)
    else:
        u = Student.objects.get(stu_username = username)
        authDict = get_auth_info(u.stu_username,u.stu_password)

    #conn to openstack API
    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'], authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])

    # #create router for the tenant, insert into RouterIntance
    # r = RouterInstance.objects.filter(owner_username=username)
    # if r:# the router already exists
    #     pass
    # else:
    #     router_name = username+"-router"
    #     external_net_name = "public"
    #     router_dict = network_resource_operation.create_router(conn,router_name,external_net_name)
    #     print "here is router-------"
    #     print router_dict
    #     new_router = RouterInstance(owner_username=username,routerIntance_id=router_dict['id'],name=router_name,status=router_dict['status'],
    #                                 gateway_net_id=router_dict[''],gateway_subnet_id=router_dict[''],gateway_ip_address=router_dict[''],
    #                                 tenant_id=router_dict[''])
    #
    # #create gateway for router


    #launch network, inser into NetworkInstance
    nets = score.exp.network.all()
    for item in nets:
        new_net_instance = network_resource_operation.create_network(conn,item.network_name,item.subnet_name,
                                                                     item.ip_version,item.cidr,item.gateway_ip)
        print "here is network *******"
        print new_net_instance[0]
        new_net = NetworkInstance(name=item.name,owner=u,network=item,exp_instance=score,
                              network_instance_id=new_net_instance[0]['id'],subnet_instance_id=new_net_instance[0]['sub_id'],
                              tenant_id = new_net_instance[0]['tenant_id'],status=new_net_instance[0]['status'],
                              allocation_pools_start=new_net_instance[0]['sub_allocation_pools']['start'],
                              allocation_pools_end=new_net_instance[0]['sub_allocation_pools']['end'])
        new_net.save()


        subnet_id = ""
        #create interface to attach network to router
        router = RouterInstance.objects.get(owner_username=username)
        r = network_resource_operation.add_interface_to_router(conn,router,subnet_id)

    #launch VM , insert into VMInstance
    vms = score.exp.vm_set.all()
    for item in vms:
        vm_instance = compute_resource_operation.create_server2()
        print "here is vms &&&&&&&&&"
        print vm_instance
        new_vmInstance = VMInstance()

    #update Score db:starttime, situation,instance_status
    re = Score.objects.filter(id=score_id).update()

    c = {}
    return render(request,'exp_score_launch.html',c)


# 2017-03-28 qinli update---can not work successfully
def exp_score_launch(request,score_id):
    try:
        score = Score.objects.get(id=score_id)
    except Score.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username,u.password)
    else:
        u = Student.objects.get(stu_username = username)
        authDict = get_auth_info(u.stu_username,u.stu_password)

    #conn to openstack API
    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'], authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])


    #launch network, inser into NetworkInstance
    # nets = score.exp.network.all()
    nets = score.exp.exp_network.all()
    router = RouterInstance.objects.get(owner_username=username)

    for item in nets:
        new_net_instance = network_resource_operation.create_network(conn,item.network_name,item.subnet_name,
                                                                     item.ip_version,item.cidr,item.gateway_ip)
        print "here is network *******"
        print new_net_instance[0]
        new_net = NetworkInstance(name=item.name,owner=u,network=item,exp_instance=score,
                              network_instance_id=new_net_instance[0]['id'],subnet_instance_id=new_net_instance[0]['sub_id'],
                              tenant_id = new_net_instance[0]['tenant_id'],status=new_net_instance[0]['status'],
                              allocation_pools_start=new_net_instance[0]['sub_allocation_pools']['start'],
                              allocation_pools_end=new_net_instance[0]['sub_allocation_pools']['end'])
        new_net.save()

        #create interface to attach network to router
        r = network_resource_operation.add_interface_to_router(conn,router,new_net.subnet_instance_id)

    #launch VM , insert into VMInstance
    vms = score.exp.vm_set.all() #需要用foreignkey功能的话需要在VM的model中加入related_name
    for item in vms:
        vm_instance = compute_resource_operation.create_server2(conn, item.name, item.image_id, item.flavor,
                                                                item.network.network_name, item.keypair)
        print "here is vms &&&&&&&&&"
        print vm_instance
        new_vmInstance = VMInstance(name=item.name, owner_name=username, vm=item, exp_instance=score,
                                    server_id=vm_instance[0]['id'], status='ACTIVE')
        new_vmInstance.save()


    #update Score db:starttime, situation,instance_status
    re = Score.objects.get(id=score_id)
    re.startTime = datetime.datetime.now()
    re.situation = 'doing'
    re.instance_status = 'LAUNCHED'
    re.save()

    c = {}
    return render(request,'exp_score_launch.html',c)



def exp_score_unlaunch(request,score_id):
    #delete VM
    #delete interface
    #delete network
    #delete gateway
    #delete router
    pass


def exp_score_clean(request,scored_id):
    pass

def exp_network_launch(request):
    conn = createconn_openstackSDK.create_connection(auth_url, region_name, project_name, auth_username,auth_password)
    e_id = 1
    experiment_operation.luanch_exp_network(conn, e_id)
    return HttpResponse('launch exp network!')

def exp_vm_launch(request):
    pass

#teacher and student both have
def exp_instance_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    ExpInstanceList = ExpInstance.objects.filter(owner_name = username).order_by('-createtime')

    context['ExpInstanceList'] = ExpInstanceList
    return render(request,'exp_instance_list.html',context)


#only teacher has
def vm_instance_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    VMInstanceList = VMInstance.objects.filter(owner_name = username).order_by('-createtime')
    VMInstanceList = VMInstanceList.exclude(status="DELETED")#do not list DELETED instance
    context['VMInstanceList'] = VMInstanceList
    return render(request,'vm_instance_list.html',context)


def vm_instance_detail(request,vi_id):
    try:
        vi = VMInstance.objects.get(id=vi_id)
    except VMInstance.DoesNotExist:
        raise Http404
    c= {}
    c['DetailDict']=vi
    return render(request,"vm_instance_detail.html",c)

def vm_instance_save_it(request,vi_id):
    try:
        vi = VMInstance.objects.get(id=vi_id)
    except VMInstance.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)
    password = u.password
    vm_instance_pause_function(vi, username, password)
    #update the 'status' field of VMInstance db
    VMInstance.objects.filter(id = vi_id).update(status='PAUSED')
    return HttpResponse("Already save it")



def vm_instance_recover_it(request,vi_id):
    try:
        vi = VMInstance.objects.get(id=vi_id)
    except VMInstance.DoesNotExist:
        raise Http404

    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)
    password = u.password

    vm_instance_unpause_function(vi,username,password)
    VMInstance.objects.filter(id=vi_id).update(status='ACTIVE')

    return HttpResponse("Alreday recover it")



def vm_instance_goto(request,vi_id):
    try:
        vi = VMInstance.objects.get(id=vi_id)
    except VMInstance.DoesNotExist:
        raise Http404

    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)
    password = u.password

    url = vm_instance_goto_function(vi,username,password)

    c={}
    c['E_I_Detail_Dict']=vi
    c['baiduurl']=url
    return render(request,"vm_instance_goto.html",c)


#-----------------------------------------------------
#Function : Get the vnc url for the vm instance (use CLI)
#Input : vm instance
#Output : vnc url
def vm_instance_goto_function(vi,username,password):
    os.environ['OS_PROJECT_DOMAIN_ID'] = 'default'
    os.environ['OS_USER_DOMAIN_ID'] = 'default'
    os.environ['OS_PROJECT_NAME'] = str(username)
    os.environ['OS_TENANT_NAME'] = str(username)
    os.environ['OS_USERNAME'] = str(username)
    os.environ['OS_PASSWORD'] = str(password)
    os.environ['OS_AUTH_URL'] = 'http://controller:5000/v3'
    os.environ['OS_IDENTITY_API_VERSION'] = '3'
    os.environ['OS_IMAGE_API_VERSION'] = '2'

    b = str(vi.server_id)
    c = 'nova get-vnc-console' + ' ' + b + ' ' + 'novnc > /home/mcy/tmp'

    output = os.system(c)
    pattern = re.compile(r'(http)\S+')
    url = ''
    file = open('/home/mcy/tmp')
    while 1:
        line = file.readline()
        if not line:
            break
        match = pattern.search(line)
        if match:
            url = match.group()
    return url
#-----------------------------------------------------

def vm_instance_start_function(vi,username,password):
    os.environ['OS_PROJECT_DOMAIN_ID'] = 'default'
    os.environ['OS_USER_DOMAIN_ID'] = 'default'
    os.environ['OS_PROJECT_NAME'] = str(username)
    os.environ['OS_TENANT_NAME'] = str(username)
    os.environ['OS_USERNAME'] = str(username)
    os.environ['OS_PASSWORD'] = str(password)
    os.environ['OS_AUTH_URL'] = 'http://controller:5000/v3'
    os.environ['OS_IDENTITY_API_VERSION'] = '3'
    os.environ['OS_IMAGE_API_VERSION'] = '2'

    b = str(vi.server_id)
    c = 'nova start'+' '+b
    os.system(c)



def vm_instance_stop_function(vi,username,password):
    os.environ['OS_PROJECT_DOMAIN_ID'] = 'default'
    os.environ['OS_USER_DOMAIN_ID'] = 'default'
    os.environ['OS_PROJECT_NAME'] = str(username)
    os.environ['OS_TENANT_NAME'] = str(username)
    os.environ['OS_USERNAME'] = str(username)
    os.environ['OS_PASSWORD'] = str(password)
    os.environ['OS_AUTH_URL'] = 'http://controller:5000/v3'
    os.environ['OS_IDENTITY_API_VERSION'] = '3'
    os.environ['OS_IMAGE_API_VERSION'] = '2'

    b = str(vi.server_id)
    c = 'nova stop'+' '+b
    os.system(c)



def vm_instance_pause_function(vi,username,password):
    os.environ['OS_PROJECT_DOMAIN_ID'] = 'default'
    os.environ['OS_USER_DOMAIN_ID'] = 'default'
    os.environ['OS_PROJECT_NAME'] = str(username)
    os.environ['OS_TENANT_NAME'] = str(username)
    os.environ['OS_USERNAME'] = str(username)
    os.environ['OS_PASSWORD'] = str(password)
    os.environ['OS_AUTH_URL'] = 'http://controller:5000/v3'
    os.environ['OS_IDENTITY_API_VERSION'] = '3'
    os.environ['OS_IMAGE_API_VERSION'] = '2'

    b = str(vi.server_id)
    c = 'nova pause'+' '+b
    os.system(c)



def vm_instance_unpause_function(vi,username,password):
    os.environ['OS_PROJECT_DOMAIN_ID'] = 'default'
    os.environ['OS_USER_DOMAIN_ID'] = 'default'
    os.environ['OS_PROJECT_NAME'] = str(username)
    os.environ['OS_TENANT_NAME'] = str(username)
    os.environ['OS_USERNAME'] = str(username)
    os.environ['OS_PASSWORD'] = str(password)
    os.environ['OS_AUTH_URL'] = 'http://controller:5000/v3'
    os.environ['OS_IDENTITY_API_VERSION'] = '3'
    os.environ['OS_IMAGE_API_VERSION'] = '2'

    b = str(vi.server_id)
    c = 'nova unpause'+' '+b
    os.system(c)



def vm_instance_snapshot(request,vi_id):
    try:
        vi = VMInstance.objects.get(id=vi_id)
    except VMInstance.DoesNotExist:
        raise Http404

    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)

    if request.method == 'POST':
        rf = CreateVMSnapshot(request.POST)
        if rf.is_valid():
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']

            # conn to openstack API
            conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                             authDict['project_name'],
                                                             authDict['auth_username'], authDict['auth_password'])
            # # step1:stop the vm----------can success because the APi is not work
            # compute_resource_operation.stop_server(conn,vi.server_id)

            # print vi.server_id
            # step2:make snapshot for the vm
            compute_resource_operation.create_server_image(conn,vi.server_id,name)
            snapshot = image_resource_operation.find_image(conn,name)
            # print "image in openstack----"
            # print snapshot['id']

            # step3:insert into VMImage
            # print "Step3----here is insert into ExpInstance db"
            new_image = VMImage(image_id=snapshot['id'],name=name, description=desc, owner_name=username,is_shared=False)
            new_image.save()
            # print new_image.id

            # step4: update the "result_image" field in VMInstance
            VMInstance.objects.filter(id=vi_id).update(result_image=new_image.id)

            return HttpResponseRedirect('/repo_private_image_list/')

    else:
        rf = CreateVMSnapshot()
    return render(request,"vm_instance_snapshot.html",{'rf':rf})


#-----------------------------------------------
#Function: Create a snapshot for a vm instance
#Input: vm instance
#Output: snapshot image
def vm_instance_snapshot_function(conn,vi,username,new_sp_name,new_sp_desc):
    #make sp in openstack
    compute_resource_operation.create_server_image(conn, vi.server_id, new_sp_name)
    snapshot = image_resource_operation.find_image(conn, new_sp_name)

    #insert into db
    new_image = VMImage(image_id=snapshot['id'], name=new_sp_name, description=new_sp_desc, owner_name=username, is_shared=False)
    new_image.save()

    #update the "result_image" field in VMInstance
    VMInstance.objects.filter(id=vi.id).update(result_image=new_image.id)
    return new_image.id
#-----------------------------------------------



def vm_instance_save(request,vi_id):#save as a VM template
    try:
        vi = VMInstance.objects.get(id=vi_id)
    except VMInstance.DoesNotExist:
        raise Http404

    #first check if the VMInstance slready has a snapshot by check the "result_image" field
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)

    if request.method == 'POST':
        rf = SaveVMasTemplate(request.POST)
        if rf.is_valid():
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']

            # conn to openstack API
            conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                             authDict['project_name'],
                                                             authDict['auth_username'], authDict['auth_password'])
            vm_instance_save_function(conn, vi, username, name, desc)

            return HttpResponseRedirect('/repo_private_VM_list/')
    else:
        rf = SaveVMasTemplate()
    return render(request, "vm_instance_save.html", {'rf': rf})



# def vm_instance_save_function(vi,username,new_vm_name,new_vm_desc):
#     if vi.result_image:
#         try:
#             snapshot_image = VMImage.objects.get(id=vi.result_image)
#         except VMImage.DoesNotExist:
#             raise Http404
#         # step2:insert a new record into VM
#         new_vm = VM(name=new_vm_name, desc=new_vm_desc, owner_name=username, image=snapshot_image, network=vi.vm.network, flavor=vi.vm.flavor,
#                     keypair=vi.vm.keypair, security_group=vi.vm.security_group)
#         new_vm.save()
#         return new_vm.id
#     else:
#         print "please first make a snapshot for the VM Instance."


#-----------------------------------------------
#Function: save the vm instance as vm template
#Input: vm instance
#Output: vm template
def vm_instance_save_function(conn,vi,username,new_vm_name,new_vm_desc):
    # step1:make sp for the vm
    new_sp_name = '_' + vi.name + '_sp' + time.strftime('%Y-%m-%d %X', time.localtime())
    new_sp_desc = "Please input description for the sp."
    sp_id = vm_instance_snapshot_function(conn, vi, username, new_sp_name, new_sp_desc)
    snapshot_image = VMImage.objects.get(id=sp_id)
    # step2:insert a new record into VM
    new_vm = VM(name=new_vm_name, desc=new_vm_desc, owner_name=username, image=snapshot_image, network=vi.connect_net.network, flavor=vi.vm.flavor,
                keypair=vi.vm.keypair, security_group=vi.vm.security_group)
    new_vm.save()
    return new_vm.id
#-----------------------------------------------



#-----------------------------------------------
#Function : Delete a VM Instance
#Input : VM Instance
#Output : None
def vm_instance_delete_function(conn,vi):
    #delete in openstack
    compute_resource_operation.delete_server(conn,vi.server_id)

    #update the "status" field in VMInstance db
    VMInstance.objects.filter(id=vi.id).update(status="DELETED")
#-----------------------------------------------



def vm_instance_delete(request,vi_id):
    try:
        vi = VMInstance.objects.get(id=vi_id)
    except VMInstance.DoesNotExist:
        raise Http404

    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)

    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                     authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])
    #delete in openstack
    compute_resource_operation.delete_server(conn,vi.server_id)

    #update the "status" field in VMInstance db
    VMInstance.objects.filter(id=vi_id).update(status="DELETED")

    return HttpResponse("Delete VM Instance Success!")


def vm_instance_edit(request,vi_id):
    pass



def net_instance_list(request):
    context = {}
    context['role'] = request.session['role']
    context['username'] = request.session['username']
    context['hello'] = 'welcome to our platfowm'
    context['currentTime'] = showTime.formatTime2()
    context['currentTimeStamp'] = showTime.transform_Timestr_To_TimeStamp(showTime.formatTime1())

    username = request.session['username']
    NetworkInstanceList = NetworkInstance.objects.filter(owner_name=username).order_by('-createtime')
    NetworkInstanceList = NetworkInstanceList.exclude(status = "DELETED")
    context['NetworkInstanceList'] = NetworkInstanceList
    return render(request, 'net_instance_list.html', context)

def net_instance_detail(request,n_id):
    try:
        ni = NetworkInstance.objects.get(id=n_id)
    except NetworkInstance.DoesNotExist:
        raise Http404
    c= {}
    c['DetailDict']= ni
    return render(request,'net_instance_detail.html',c)


def net_instance_edit(request,ni_id):#according to openstack, it just allowed to edit "name"
    pass

def net_instance_save(request,ni_id):#insert into Network db
    try:
        ni = NetworkInstance.objects.get(id=ni_id)
    except NetworkInstance.DoesNotExist:
        raise Http404

    username = request.session['username']
    role = request.session['role']

    if request.method == 'POST':
        rf = SaveNetasTemplate(request.POST)
        if rf.is_valid():
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            # step1:get necessary data
            subnet_name = name+'_subnet'
            # step2:insert a new record into VM
            new_net = Network(network_name=name,network_description=desc,owner_name=username,subnet_name=subnet_name,
                              ip_version=ni.network.ip_version,cidr=ni.network.cidr,gateway_ip=ni.network.gateway_ip,
                              enable_dhcp=ni.network.enable_dhcp,dns=ni.network.dns,
                              allocation_pools_start=ni.network.allocation_pools_start,
                              allocation_pools_end=ni.network.allocation_pools_end)
            new_net.save()
            return HttpResponseRedirect('/repo_private_network_list/')
    else:
        rf = SaveNetasTemplate()
    return render(request,"net_instance_save.html",{'rf':rf})

#-----------------------------------------------
#Function : Save the net instance as a net template
#Input : net instance
#Output: net template
def net_instance_save_function(ni,username,new_net_name,new_net_desc):
    # step1:get necessary data
    subnet_name = new_net_name + '_subnet'
    # step2:insert a new record into VM
    new_net = Network(network_name=new_net_name, network_description=new_net_desc, owner_name=username, subnet_name=subnet_name,
                      ip_version=ni.network.ip_version, cidr=ni.network.cidr, gateway_ip=ni.network.gateway_ip,
                      enable_dhcp=ni.network.enable_dhcp, dns=ni.network.dns,
                      allocation_pools_start=ni.network.allocation_pools_start,
                      allocation_pools_end=ni.network.allocation_pools_end)
    new_net.save()
    return new_net.id
#-----------------------------------------------


def net_instance_delete(request,ni_id):
    try:
        ni = NetworkInstance.objects.get(id=ni_id)
    except NetworkInstance.DoesNotExist:
        raise Http404
    #make sure all VMs on the net instance are DELETED
    vis = ni.vminstance_set.all()

    deleted_vi_count =0
    for vi in vis:
        if vi.status == "DELETED":
            deleted_vi_count=deleted_vi_count+1
    if deleted_vi_count == len(vis):#all vi on ni deleted,so can delete the ni

        username = request.session['username']
        role = request.session['role']
        if role == 'teacher':
            u = User.objects.get(username=username)
            authDict = get_auth_info(u.username, u.password)
        else:
            u = Student.objects.get(stu_username=username)
            authDict = get_auth_info(u.stu_username, u.stu_password)

        conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                         authDict['project_name'],
                                                         authDict['auth_username'], authDict['auth_password'])
        # delete in openstack
        #------delete the connect with router by deleting the interface from router
        router = RouterInstance.objects.get(owner_username=username)  # admin already create a router for this user when register it,every user has one router
        network_resource_operation.remove_interface_from_router(conn,router.routerIntance_id,ni.subnet_instance_id)
        network_resource_operation.delete_network(conn,ni.network_instance_id)

        #update the "status" field of NetworkInstance db
        NetworkInstance.objects.filter(id=ni_id).update(status="DELETED")
        return HttpResponse("Delete NetworkInstance Success")
    else:
        return HttpResponse("There are VM(s) still connecting to the NetworkInstance! Please delete them first!")



# --------------------------------------------------------
#Function : To make sure all VMs on the net instance are DELETED
#Input : net instance
#Output : True or False
def if_vi_exist_on_ni(ni):
    vis = ni.vminstance_set.all()

    deleted_vi_count = 0
    for vi in vis:
        if vi.status == "DELETED":
            deleted_vi_count = deleted_vi_count + 1
    if deleted_vi_count == len(vis):  # all vi on ni deleted,so can delete the ni
        return False
    else:
        return True

#--------------------------------------------------------



#--------------------------------------------------------
#Function : Delete the net instance
#Input : net instance
#Output : None
def net_instance_delete_function(conn,ni,username):
    # delete in openstack
    # ------delete the connect with router by deleting the interface from router
    router = RouterInstance.objects.get(owner_username=username)  # admin already create a router for this user when register it,every user has one router
    network_resource_operation.remove_interface_from_router(conn, router.routerIntance_id, ni.subnet_instance_id)
    network_resource_operation.delete_network(conn, ni.network_instance_id)

    # update the "status" field of NetworkInstance db
    NetworkInstance.objects.filter(id=ni.id).update(status="DELETED")
#--------------------------------------------------------



def network_launch(request,n_id):
    try:
        n = Network.objects.get(id=n_id)
    except Network.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username,u.password)
    else:
        u = Student.objects.get(stu_username = username)
        authDict = get_auth_info(u.stu_username,u.stu_password)

    # conn to openstack API
    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                     authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])
    #launch network, insert into networkInstance
    router = RouterInstance.objects.get(owner_username=username)#admin already create a router for this user when register it
    new_net_instance = network_resource_operation.create_network(conn, n.network_name, n.subnet_name,
                                                                 n.ip_version, n.cidr, n.gateway_ip)
    new_net = NetworkInstance(name=n.network_name, owner_name=username, network=n,
                              network_instance_id=new_net_instance['id'], subnet_instance_id=new_net_instance['sub_id'],
                              tenant_id=new_net_instance['tenant_id'], status=new_net_instance['status'],
                              allocation_pools_start=new_net_instance['sub_allocation_pools'][0]['start'],
                              allocation_pools_end=new_net_instance['sub_allocation_pools'][0]['end'])
    new_net.save()

    # create interface to attach network to router
    r = network_resource_operation.add_interface_to_router(conn, router.routerIntance_id, new_net.subnet_instance_id)
    return HttpResponseRedirect('/net_instance_list/')


def vm_launch(request,v_id):
    try:
        vm = VM.objects.get(id=v_id)
    except VM.DoesNotExist:
        raise Http404

    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)

    # conn to openstack API
    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                     authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])
    # launch VM ,
    server_name = vm.name
    image_name = vm.image.name
    flavor_name = vm.flavor
    network_name = vm.network.network_name  # should find the net instance
    private_keypair_name = vm.keypair

    # first check if the needed netInstance exist in NetworkInstance db?
    ni = NetworkInstance.objects.filter(owner_name=username,network=vm.network,status="ACTIVE")
    if len(ni)>0:#the Network Instance exist
        netInstance = NetworkInstance.objects.get(owner_name=username,network=vm.network,status="ACTIVE")
        vm_instance = compute_resource_operation.create_server2(conn, server_name, image_name, flavor_name,
                                                                network_name, private_keypair_name)
        # insert into VMInstance db
        new_vmInstance = VMInstance(name=vm.name, owner_name=username, vm=vm,
                                    # belong_exp_instance_id=new_expInstance.id,
                                    server_id=vm_instance['id'], status=vm_instance['status'],
                                    createtime=datetime.datetime.now(),
                                    updatetime=datetime.datetime.now(),
                                    connect_net=netInstance)
        new_vmInstance.save()
    else:
        return HttpResponse("The Network Instance does not exist, please launch it first!")
    return HttpResponseRedirect('/vm_instance_list/')

#---------------------------------------function to repeat use---------------------------------------
def createNetInstance(conn,n):#input is netTemplate,output is netInstance
    pass


def createVMInstance(conn,vm):#input is vmTemplate,output is vmInstance
    pass
#---------------------------------------function to repeat use---------------------------------------



#teacher and student diff
def exp_instance_detail(request,exp_i_id):#let uer see the exp_instance info detail
    try:
        ei = ExpInstance.objects.get(id=exp_i_id)
    except ExpInstance.DoesNotExist:
        raise Http404
    ei_dict={}
    ei_dict['id']=ei.id
    ei_dict['name']=ei.name
    ei_dict['exp']=ei.exp
    ei_dict['owner_name']=ei.owner_name
    ei_dict['createtime']=ei.createtime
    ei_dict['updatetime']=ei.updatetime
    ei_dict['instance_status']=ei.instance_status
    ei_dict['score_id']=ei.score_id#only student use this field

    #get all net instance of the exp instance
    niList = NetworkInstance.objects.filter(belong_exp_instance_id=exp_i_id)
    #get all vm instance of the exp instance
    viList = VMInstance.objects.filter(belong_exp_instance_id=exp_i_id)
    ei_dict['net_instances'] = niList
    ei_dict['vm_instances'] = viList

    c = {}
    c['username']=request.session['username']
    c['role']=request.session['role']
    c['E_I_Detail_Dict'] = ei_dict

    topo_ndict = {}
    count = 0
    topo_info = '{"nodes":['
    for vm in viList:
        count = count + 1
        topo_info = topo_info + '{"name":"' + vm.name + '","id":' + str(count) + ',"image":"Q-node"},'
        topo_ndict[vm.name] = count
    for network in niList:
        count = count + 1
        topo_info = topo_info + '{"name":"' + network.name + '","id":' + str(count) + ',"image":"Q-cloud"},'
        topo_ndict[network.name] = count
    count = count + 1
    topo_info = topo_info + '{"id":' + str(count) + ',"x":-100,"y":-50}], "edges": ['
    topo_ndict['router'] = count

    count = 0
    for vm in viList:
        count = count + 1
        if count != 1:
            topo_info = topo_info + ','
        topo_info = topo_info + '{"name":"","from":' + str(topo_ndict[vm.name]) + ',"to":' + str(
            topo_ndict[vm.connect_net.name]) + '}'


    topo_info = topo_info + ']}'
    Topo = []
    Topo.append(topo_info)

    #  Topo=['{"nodes":[{"name": "C", "id": 3},{"name": "A", "x": -100, "y": -50, "id": 1}, {"name": "B", "id": 2}], "edges": [{"name": "Edge", "from":1, "to":2}]}']

    # ly topo 2017/4/6    return render(request, 'exp_detail.html',{'Topo':json.dumps(Topo),'c':c})
    return render(request, 'exp_instance_detail.html', {'Topo': json.dumps(Topo), 'c': c})






def exp_instance_goto(request,exp_i_id):#make user login the operate server
    try:
        ei = ExpInstance.objects.get(id=exp_i_id)
    except ExpInstance.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']


    c={}
    c['E_I_Detail_Dict']=ei
    c['baiduurl']=" http://202.112.113.220:6080/vnc_auto.html?token=a0dff238-0199-442c-be38-a74a4dfd11c8"
    return render(request,"exp_instance_goto.html",c)


def exp_instance_recover_it(request,exp_i_id):
    pass



#Function :
def exp_instance_save_it(request,exp_i_id):
    pass

def exp_instance_save(request,exp_i_id):#save the instance as a template:
    try:
        ei = ExpInstance.objects.get(id=exp_i_id)
    except ExpInstance.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']

    if request.method == 'POST':
        rf = SaveExpasTemplate(request.POST)
        if rf.is_valid():
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            # step1:get the Experiment needed data from ExpInstance
            # ----get data
            exp_image_count = 0
            exp_guide_path = ei.exp.exp_guide_path  # Actually, it should copy and rename the guide
            is_shared = False  # by default we set it private
            VM_count = 0
            # step2:insert a new record into Experiment
            new_exp = Experiment(exp_name=name, exp_description=desc, exp_owner_name=username,
                                 exp_image_count=exp_image_count,
                                 exp_guide_path=exp_guide_path, is_shared=is_shared, VM_count=VM_count)
            new_exp.save()

            if role == 'teacher':
                u = User.objects.get(username=username)
                authDict = get_auth_info(u.username, u.password)
            else:
                u = Student.objects.get(stu_username=username)
                authDict = get_auth_info(u.stu_username, u.stu_password)
            conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                             authDict['project_name'],
                                                             authDict['auth_username'], authDict['auth_password'])

            included_image_list =[]
            #-----get included VM
            include_vi = VMInstance.objects.filter(belong_exp_instance_id=exp_i_id)
            include_vi = include_vi.exclude(status="DELETED")
            for vi in include_vi:
                #then save the vminstance
                v_id = vm_instance_save_function(conn,vi,username,vi.vm.name,vi.vm.desc)
                VM.objects.filter(id=v_id).update(exp=new_exp)

                v = VM.objects.get(id=v_id)
                if v.image not in included_image_list:
                    included_image_list.append(v.image)

            #-----get included image
            for i in included_image_list:
                new_exp.exp_images.add(i)

            #-----get included network
            included_ni = NetworkInstance.objects.filter(belong_exp_instance_id=exp_i_id)
            included_ni = included_ni.exclude(status="DELETED")
            for ni in included_ni:
                n_id = net_instance_save_function(ni,username,ni.network.network_name,ni.network.network_description)
                n = Network.objects.get(id=n_id)
                new_exp.exp_network.add(n)

            Experiment.objects.filter(id=new_exp.id).update(exp_image_count=len(included_image_list),VM_count=len(include_vi))
            return HttpResponseRedirect('/repo_private_exp_list/')
    else:
        rf = SaveExpasTemplate()
    return render(request,"exp_instance_save.html",{'rf':rf})


#Function: save the instance as a template
#Input: exp Instance
#Output: exp Template
def exp_instance_save_function(conn,ei,username,new_exp_name,new_exp_desc):
    name = new_exp_name
    desc = new_exp_desc
    exp_image_count = 0
    exp_guide_path = ei.exp.exp_guide_path  # Actually, it should copy and rename the guide
    is_shared = False  # by default we set it private
    VM_count = 0
    new_exp = Experiment(exp_name=name, exp_description=desc, exp_owner_name=username,
                         exp_image_count=exp_image_count,
                         exp_guide_path=exp_guide_path, is_shared=is_shared, VM_count=VM_count)
    new_exp.save()

    included_image_list = []
    # -----get included VM
    include_vi = VMInstance.objects.filter(belong_exp_instance_id=ei.id)
    include_vi = include_vi.exclude(status="DELETED")
    for vi in include_vi:
        # then save the vminstance
        v_id = vm_instance_save_function(conn, vi, username, vi.vm.name, vi.vm.desc)
        VM.objects.filter(id=v_id).update(exp=new_exp)

        v = VM.objects.get(id=v_id)
        if v.image not in included_image_list:
            included_image_list.append(v.image)

    # -----get included image
    for i in included_image_list:
        new_exp.exp_images.add(i)

    # -----get included network
    included_ni = NetworkInstance.objects.filter(belong_exp_instance_id=ei.id)
    included_ni = included_ni.exclude(status="DELETED")
    for ni in included_ni:
        n_id = net_instance_save_function(ni, username, ni.network.network_name, ni.network.network_description)
        n = Network.objects.get(id=n_id)
        new_exp.exp_network.add(n)

    Experiment.objects.filter(id=new_exp.id).update(exp_image_count=len(included_image_list), VM_count=len(include_vi))
    return new_exp.id



#define function to reuse
def upload_report_file(report_file):
    save_path = "/home/mcy/upload/files/reports"
    destination = open(os.path.join(save_path, report_file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in report_file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    file_path = save_path + '/' + report_file.name
    return file_path

def exp_instance_submit(request,exp_i_id):
    try:
        ei = ExpInstance.objects.get(id=exp_i_id)
    except ExpInstance.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']
    stu = Student.objects.get(stu_username__exact=username)
    s = Score.objects.get(id = ei.score_id)
    print s

    if request.method == 'POST':
        rf = SubmitExpInstanceForm(request.POST)
        reportFile = request.FILES.get("report_file",None)
        if not reportFile:
            return HttpResponse("no file to choose")
        save_path = "/home/mcy/upload/files/report"
        destination = open(os.path.join(save_path,reportFile.name),'wb+')
        for chunk in reportFile.chunks():
            destination.write(chunk)
        destination.close()
        report_path = save_path + '/' + reportFile.name

        report_name = rf.data['report_name']
        print report_name

        #-----create OpenStack Conn
        authDict = get_auth_info(stu.stu_username, stu.stu_password)
        conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                         authDict['project_name'],
                                                         authDict['auth_username'], authDict['auth_password'])

        #-----save the exp_instance as template
        new_exp_name = username+'_submit_exp_by_Score_id_'+ str(s.id)
        new_exp_desc = "This exp is a submit exp template"
        result_exp_id = exp_instance_save_function(conn, ei, username, new_exp_name, new_exp_desc)


        #-----update the Score db on "finishedTime', "situation", "result_exp_id" and "report_path" field
        Score.objects.filter(id=ei.score_id).update(finishedTime = datetime.datetime.now(),situation="done",result_exp_id=result_exp_id,report_path=report_path)

        return HttpResponseRedirect('/exp_list_done/')
    else:
        rf = SubmitExpInstanceForm()

    return render(request,'exp_instance_submit.html',{'rf':rf})


#Both teacher and student
def exp_instance_delete(request,exp_i_id):#delete the exp instance
    try:
        ei = ExpInstance.objects.get(id=exp_i_id)
    except ExpInstance.DoesNotExist:
        raise Http404
    username = request.session['username']
    role = request.session['role']
    if role == 'teacher':
        u = User.objects.get(username=username)
        authDict = get_auth_info(u.username, u.password)
    else:
        u = Student.objects.get(stu_username=username)
        authDict = get_auth_info(u.stu_username, u.stu_password)
    conn = createconn_openstackSDK.create_connection(authDict['auth_url'], authDict['region_name'],
                                                     authDict['project_name'],
                                                     authDict['auth_username'], authDict['auth_password'])

    #delete VMInstance
    viList = VMInstance.objects.filter(belong_exp_instance_id=exp_i_id)
    for vi in viList:
        vm_instance_delete_function(conn,vi)

    #delete networkInstance
    niList = NetworkInstance.objects.filter(belong_exp_instance_id=exp_i_id)
    for ni in niList:
        if if_vi_exist_on_ni(ni):
            return HttpResponse("There is still vm instance on the net instance! Please remove them first!")
        else:
            net_instance_delete_function(conn,ni,username)

    #update the "instance_status" field of ExpInstance db
    ExpInstance.objects.filter(id=exp_i_id).update(instance_status="DELETED",updatetime=datetime.datetime.now())

    return HttpResponse("The Exp Instance is deleted successfully!")


def exp_instance_start(request,exp_i_id):
    pass

def exp_instance_stop(request,exp_i_id):
    pass

def exp_instance_pause(request,exp_i_id):
    pass

def exp_instance_unpause(request,exp_i_id):
    pass

def exp_instance_suspend(request,exp_i_id):
    pass

def exp_instance_resume(request,exp_i_id):
    pass






#only role=stu has this operation
def exp_submit(request,d_id):#??
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
            re = Score.objects.filter(stu=s,delivery_id=d_id).update(report_path=file_path)
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


def score_report_download(request,score_id):
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