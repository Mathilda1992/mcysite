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

import datetime,time

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


from Iserlab import createconn_openstackSDK
from Iserlab import image_resource_operation,compute_resource_operation,network_resource_operation,identity_resource_operation
from Iserlab import experiment_operation,repo_operation,user_operation
from Iserlab import showTime

#-------import models---------
from Iserlab.models import User,Group,Student,Experiment,VMImage,Network,Delivery,Score

#-------import forms----------
from Iserlab.forms import *

#--------default argus used for connect to OpenStack Cloud----
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

    #default show the exp situation list
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
#                  Teaching center operate                             #
#***********************************************************************#
#-----------Delivery Operate(only role=teacher has these function)-------------#
def delivery_list(request):
    username = request.session['username']
    teacher = User.objects.get(username=username)
    DeliveryList = Delivery.objects.filter(teacher=teacher).order_by('-delivery_time')
    context={}
    context['DeliveryList'] = DeliveryList
    return render(request, 'delivery_list.html', context)


def delivery_delete(request,d_id):
    try:
        d = Delivery.objects.get(id=d_id)
    except Delivery.DoesNotExist:
        raise Http404
    re = Delivery.objects.filter(id=d_id).delete()
    if re:
        print "Delivery delete success!"
    return HttpResponseRedirect('/teach_home/')


def delivery_detail(request,d_id):
    try:
        d = Delivery.objects.get(id =d_id)
    except Delivery.DoesNotExist:
        raise Http404
    #get delivery detail from db
    context = {}
    s_list = d.group.student.all()
    D_detial_dict = {'id':d_id,'name':d.name,'desc':d.desc,'exp':d.exp,'teacher':d.teacher,'group':d.group,'stulist':s_list,
                     'delivery_time':d.delivery_time,'start_time':d.start_time,'stop_time':d.stop_time,'total_stu':len(s_list),
                     }
    context['D_detail_dict']=D_detial_dict
    return render(request,'delivery_detail.html',context)


def delivery_edit(request,d_id):
    try:
        d = Delivery.objects.get(id=d_id)
    except Delivery.DoesNotExist:
        raise Http404
    #initial the form
    attrs = {}
    attrs['name']=d.name
    attrs['desc']=d.desc
    attrs['exp']=d.exp.exp_name
    attrs['group']=d.group.name
    attrs['startDateTime']=d.start_time
    attrs['endDateTime']=d.stop_time
    gf = EditDeliveryForm(initial=attrs)

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
        rf = AddDeliveryForm()
    return render_to_response("delivery_edit.html",{'rf':gf})


#pay attention to multi exps to multi group
def delivery_create(request):
    username = request.session['username']
    if request.method =='POST':
        rf = AddDeliveryForm(request.POST)
        if rf.is_valid():
            #get data from the form
            name = rf.cleaned_data['name']
            desc = rf.cleaned_data['desc']
            exp_idList = rf.cleaned_data['exp']
            group_idList = rf.cleaned_data['group']
            startDateTime = rf.cleaned_data['startDateTime']
            endDateTime = rf.cleaned_data['endDateTime']
            #prepare other required data
            teacher = User.objects.get(username=username)
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
                    d.save()
            #insert into db:score
            d_List = Delivery.objects.filter(name=name,teacher=teacher)
            for i in range(0,len(d_List)):
                stulist = d_List[i].group.student.all()
                for j in range(0,len(stulist)):#insert a record into score db for every stu
                    new_score = Score(exp=d_List[i].exp,stu=stulist[j],scorer= teacher,delivery_id=d_List[i].id)
                    new_score.save()
        return HttpResponseRedirect('/teach_home/')
    else:
        rf = AddDeliveryForm()
    return render_to_response("delivery_create.html",{'rf':rf})


def delivery_list_by_teacher():
    pass

#------role = stu operate -----
def delivery_list_by_student():
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

    list =[]
    for stu in stu_list:
        #get data from score db
        score = Score.objects.get(stu=stu,exp=e,scorer=t,delivery_id=d_id)

        list.append(score)
    context={}
    context['Delivery'] = d
    context['ScoreList'] = list

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
                print Score.objects.get(id=score_id).result_exp_id
            return HttpResponseRedirect('/teach_result_list/')
    else:
        sf = ScoreForm()
    return render_to_response("teach_result_score.html", {'sf': rf})



def teach_result_report_download(request,score_id):
    pass




#---list all exp results(situation=done)-----from score db
def teach_result_list(request):
    username = request.session['username']
    current_teacher = User.objects.get(username=username)
    ResultList = Score.objects.filter(scorer=current_teacher,situation='Done',result_exp_id__isnull=False).order_by('-finishedTime')
    context = {}
    context['ResultList'] = ResultList
    return render(request, 'teach_result_list.html', context)



#equal to teach_score_list_by_exp
def teach_score_list(request):
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
    context = {}
    context['ExpScoreList']=ExpScoreList
    return render(request,'teach_score_list.html',context)


#only role=teacher
def teach_score_list_by_stu(request):
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
    context = {}
    context['StuScoreList']=StuScoreList
    return render(request,'teach_score_list_by_stu.html',context)



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

def repo_image_detail(request,i_id):
    pass


def repo_image_edit(request,i_id):
    pass

def repo_image_delete(request,i_id):
    pass

def repo_image_share(request,i_id):
    pass

def repo_network_detail(request,n_id):
    pass

def repo_network_edit(request,n_id):
    pass

def repo_network_delete(request,n_id):
    pass

def repo_ImageCart_list(request):
    pass

def repo_NetworkCart_list(request):
    pass

def repo_ImageCart_add(request,i_id):
    pass

def repo_NetworkCart_add(rquest,n_id):
    pass

def repo_ImageCart_delete(request,i_id):
    pass

def repo_Network_delete(request,n_id):
    pass


#---------------------------------------------------#


def repo_public_image_list(request):
    PublicImageList = VMImage.objects.filter(is_shared=True).order_by("-shared_time")
    context ={}
    context['PublicImageList']=PublicImageList
    return render(request,"repo_public_image_list.html",context)



def repo_private_exp_list(request):
    username = request.session['username']
    teacher = User.objects.get(username=username)
    PrivateExpList = Experiment.objects.filter(exp_owner=teacher).order_by('-exp_createtime')
    context={}
    context['PrivateExpList'] = PrivateExpList
    return render(request,"repo_private_exp_list.html",context)



def repo_private_image_list(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    PrivateImageList = VMImage.objects.filter(owner=t).order_by('-created_at')
    context = {}
    context['PrivateImageList']=PrivateImageList
    return render(request,"repo_private_image_list.html",context)


def repo_private_network_list(request):
    pass

def repo_create_network(request):
    pass


def repo_create_image(request):

    if request.method == 'POST':
        form = CreateImageForm(request.POST,request.FILES)
        if form.is_valid():
            repo_handle_upload_image()
    pass


def repo_handle_upload_image(f):
    pass



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
    stulist = forms.MultipleChoiceField(label='Stulist',
                                        required=False,
                                        widget=forms.CheckboxSelectMultiple,choices=STU_CHECKBOX_CHOICES,)



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
    try:
        g = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise Http404
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


#only role = stu has this function
def exp_list_by_stu(request):
    username = request.session['username']
    role = request.session['role']
    pass




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
    #initial the form
    attrs = {}
    attrs['name']=e.exp_name + "_copy"
    attrs['desc']=e.exp_description
    attrs['images_idList']= images_idList
    attrs['networks_idList']=networks_idList
    attrs['guide']=e.exp_guide
    attrs['refer_result']=e.exp_result
    gf = AddExpForm(initial=attrs)

    #insert a new record into db
    username = request.session['username']
    t = User.objects.get(username=username)
    if request.method == 'POST':
        rf = AddExpForm(request.POST)
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
        rf = AddExpForm()
    return render_to_response("exp_copy.html",{'rf':gf})



#only role = teacher has this function
def exp_create(request):
    username = request.session['username']
    t = User.objects.get(username=username)
    if request.method == 'POST':
        rf = AddExpForm(request.POST)
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
        rf = AddExpForm()
    return render_to_response("exp_create.html",{'rf':rf})



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

    #initial the form
    attrs = {}
    attrs['name']=e.exp_name
    attrs['desc']=e.exp_description
    attrs['images_idList']= images_idList
    attrs['networks_idList']=networks_idList
    attrs['guide']=e.exp_guide
    attrs['refer_result']=e.exp_result
    gf = AddExpForm(initial=attrs)

    #edit and update the exp
    if request.method == 'POST':
        rf = AddExpForm(request.POST)
        if rf.is_valid():
            #get input data from form
            update_name = rf.cleaned_data['name']
            update_desc = rf.cleaned_data['desc']
            update_images_idList = rf.cleaned_data['images_idList']
            update_networks_idList = rf.cleaned_data['networks_idList']
            update_guide = rf.cleaned_data['guide']
            update_refer_result = rf.cleaned_data['refer_result']

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
        rf = AddExpForm()
    return render_to_response("exp_edit.html",{'rf':gf})



#only role = teacher has this function
def exp_share(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    #update the is_shared field in Experiment db
    re = Experiment.objects.filter(id=exp_id).update(is_shared=True,shared_time=datetime.datetime.now())
    return HttpResponseRedirect('/exp_home/')


#only role = teacher has this function
def exp_delivery(request,exp_id):
    username = request.session['username']
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404

    attrs = {}
    attrs['name']="delivery_"+ e.exp_name+"_"+ time.strftime('%Y-%m-%d %X',time.localtime())
    gf = AddExpForm(initial=attrs)

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
            teacher = User.objects.get(username=username)
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
        rf = ExpDeliveryForm()
    return render_to_response("exp_delivery.html", {'rf': gf})



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
        e = Experiment.objects.get(id=exp_id)
        pass
    else:
        pass


#teacher and student both have
def exp_pause(request,exp_id):
    pass


#teacher and student both have
def exp_save(request,exp_id):
    pass

def exp_resume(request,exp_id):
    pass

#teacher and student both have
def exp_clean(request,exp_id):
    pass

#only role=stu has this operation
def exp_submit(request,exp_id):
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
#                  Teacher list resource in private repo                 #
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