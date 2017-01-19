
# mcy write sone test code to exercise how to use Django


from django.shortcuts import render
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.core.mail import send_mail

# -*- coding: utf-8 -*-

#from __future__ import unicode_literals

import json


def index(request):
    string = "hello world"
    NameList = ["Alice","Bob","Cara"]
    info_dict = {'site':'baidu.com','tag':'Search Engine','country':'China'}

    List = map(str,range(100))
    # return render(request,'test.html',{'List':List})

    # return render(request,'test.html',{'info_dict':info_dict})
    stu_email_List = ['machenyi2011@163.com']
    send_mail('Subject here', 'Here is the message', 'machenyi2011@163.com', stu_email_List, fail_silently=False)

    var =87
    return render(request, 'test.html', {'var':var})


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


def home(request):
    List = ['alice', 'bob','cara']
    Dict = {'site': 'www.baidu.com', 'author': 'machenyi'}
    return render(request, 'test111.html', {
        'List': json.dumps(List),
        'Dict': json.dumps(Dict)
    })


