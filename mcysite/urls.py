"""mcysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


from Iserlab.login import *

from Iserlab.home import *
from Iserlab.views import *
from people.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',hello,name='home'),
    url(r'^time/$',current_datetime,name = 'current_datetime'),
    url(r'^test444/plus/(\d{1,2})/$',hours_ahead),
    url(r'^test222/$',test_template),
    url(r'^test333/$',current_datetime),


    #basic openstack resource operate
    url(r'^server_list/$',server_list,name='server_list'),
    url(r'^network_list/$',network_list,name='network_list'),
    url(r'^subnet_list/$', subnet_list, name='subnet_list'),
    url(r'^network_create/$',network_create,name='network_create'),
    url(r'^flavor_list/$',flavor_list,name='flavor_list'),
    url(r'^image_list/$',image_list,name='image_list'),
    url(r'^image_list2/$',image_list2,name='image_list2'),
    url(r'^user_list/$',openstack_user_list,name='user_list'),
    url(r'^project_list/$',openstack_project_list,name='project_list'),
    url(r'^project_find/$', openstack_project_find, name='project_find'),
    url(r'^project_create/$', openstack_project_create, name='project_create'),
    url(r'^role_list/$', openstack_role_list, name='role_list'),
    url(r'^vm_create/$',VM_create,name='vm_create'),
    url(r'^image_find/$',image_find,name='image_find'),


    #test
    url(r'^index/$',index,name='index'),
    url(r'^add/$',add,name='add'),
    url(r'^add/(\d+)/(\d+)/$',old_add2_redirect),
    url(r'^new_add/(\d+)/(\d+)/$',add2,name='add2'),
    url(r'^bloglist/$',blog_list2),
    #test book example
    url(r'^search/$',search),#failed
    url(r'^contact/$',contact),#need to test


    #system operate
    url(r'^login/$',login,name='login'),
    url(r'^register/$',register,name='register'),

    #user operate
    url(r'^group_list/$', group_list, name='group_list'),
    url(r'^group_create/$', group_create, name='group_create'),
    url(r'^group_get/$',group_get,name='group_get'),
    url(r'^group_stu_get/$',group_stu_get,name='group_stu_get'),
    url(r'^group_view/$', group_view, name='group_view'),
    url(r'^group_delete/$', group_delete, name='group_delete'),
    url(r'^openstack_user_list/$',openstack_user_list,name='openstack_user_list'),


    #exp operate
    url(r'^exp_list/$',exp_list,name='exp_list'),
    url(r'^exp_create/$',exp_create,name='exp_create'),
    url(r'^exp_copy/$',exp_copy,name='exp_copy'),
    url(r'^exp_detail/$',exp_detail,name='exp_detail'),
    url(r'^exp_filter_by_name/$',exp_filter_by_user,name='exp_filter_by_name'),
    url(r'^exp_network_launch/$',exp_network_launch,name='luanch_exp_network'),


    #repo operate
    url(r'^repo_exp_list/$',repo_exp_list,name='repo_exp_list'),
]
