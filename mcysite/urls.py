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
from people.views import *
from blog.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^download_file/$', download_file, name='download_file'),


    url(r'^$',home,name='home'),
    url(r'^home/$',home,name='home'),
    url(r'^time/$',current_datetime,name = 'current_datetime'),
    url(r'^test444/plus/(\d{1,2})/$',hours_ahead),
    url(r'^test222/$',test_template),
    url(r'^test333/$',current_datetime),

    #blog app
    url(r'^blogs/$',get_blogs),
    url(r'^detail/(\d+)/$',get_details ,name='blog_get_detail'),


    #basic openstack resource operate
    url(r'^openstack_API_home/$',openstack_API_home,name='openstack_API_home'),
    url(r'^server_list/$',server_list,name='server_list'),
    url(r'^server_create/$', server_create, name='server_create'),
    url(r'^server_delete/$', server_delete, name='server_delete'),
    url(r'^flavor_list/$', flavor_list, name='flavor_list'),

    url(r'^network_list/$',network_list,name='network_list'),
    url(r'^subnet_list/$', subnet_list, name='subnet_list'),
    url(r'^network_create/$',network_create,name='network_create'),
    url(r'^network_delete/$', network_delete, name='network_delete'),
    url(r'^network_update/$', network_update, name='network_update'),
    url(r'^router_list/$',router_list,name='router_list'),
    url(r'^gateway_add_to_router/$', gateway_add_to_router, name='gateway_add_to_router'),
    url(r'^interface_add_to_router/$', interface_add_to_router, name='interface_add_to_router'),
    url(r'^interface_delete_from_router/$', interface_delete_from_router, name='interface_delete_from_router'),


    url(r'^image_list/$',image_list,name='image_list'),
    url(r'^image_list2/$',image_list2,name='image_list2'),
    url(r'^image_delete/$', image_delete, name='image_delete'),
    url(r'^image_update/$', image_update, name='image_update'),

    url(r'^user_list/$',openstack_user_list,name='user_list'),
    url(r'^project_list/$',openstack_project_list,name='project_list'),
    url(r'^project_find/$', openstack_project_find, name='project_find'),
    url(r'^project_create/$', openstack_project_create, name='project_create'),
    url(r'^role_list/$', openstack_role_list, name='role_list'),
    url(r'^openstack_user_list/$', openstack_user_list, name='openstack_user_list'),

    url(r'^image_find/$',image_find,name='image_find'),
    url(r'^image_create/$', image_create, name='image_create'),

    #test
    # url(r'^index/$',index,name='index'),
    # url(r'^add/$',add,name='add'),
    # url(r'^add/(\d+)/(\d+)/$',old_add2_redirect),
    # url(r'^new_add/(\d+)/(\d+)/$',add2,name='add2'),
    url(r'^bloglist/$',blog_list2),
    #test book example
    url(r'^search/$',search,name='search'),#failed
    url(r'^contact/$',contact,name='contact'),#need to test


    #system operate
    url(r'^login/$',login,name='login'),
    url(r'^register/$',register,name='register'),

    #user operate
    url(r'^stu_home/$',stu_home,name='stu_home'),
    url(r'^group_list/$', stu_home, name='stu_home'),
    url(r'^group_create/$', group_create, name='group_create'),
    url(r'^group_get/$',group_get,name='group_get'),
    # url(r'^group_stu_get/$',group_stu_get,name='group_stu_get'),
    #url(r'^group_view/$', group_view, name='group_view'),
    url(r'^group_view/(\d+)/$', group_view, name='group_view'),
    url(r'^group_edit/(\d+)/$', group_edit, name='group_edit'),
    url(r'^group_delete/(\d+)/$', group_delete, name='group_delete'),



    #exp operate
    url(r'^exp_home/$',exp_home,name='exp_home'),
    url(r'^exp_list/$',exp_home,name='exp_home'),
    url(r'^exp_create/$',exp_create,name='exp_create'),
    url(r'^exp_create_VM/(\d+)$', exp_create_VM, name='exp_create_VM'),
    url(r'^exp_delete_VM/(\d+)$', exp_delete_VM, name='exp_delete_VM'),
    url(r'^exp_copy/(\d+)/$',exp_copy,name='exp_copy'),
    url(r'^exp_detail/(\d+)/$',exp_detail,name='exp_detail'),
    url(r'^exp_edit/(\d+)/$', exp_edit, name='exp_edit'),
    url(r'^exp_delete/(\d+)/$', exp_delete, name='exp_delete'),
    url(r'^exp_delivery/(\d+)/$', exp_delivery, name='exp_delivery'),
    url(r'^exp_share/(\d+)/$', exp_share, name='exp_share'),
    url(r'^exp_launch/(\d+)/$', exp_launch, name='exp_launch'),
    url(r'^exp_submit/(\d+)/$', exp_submit, name='exp_submit'),
    url(r'^exp_guide_download/(\d+)/$', exp_guide_download, name='exp_guide_download'),
    # url(r'^exp_network_launch/$',exp_network_launch,name='luanch_exp_network'),

    url(r'^exp_score_launch/(\d+)/$', exp_score_launch, name='exp_score_launch'),
    url(r'^exp_score_delete/(\d+)/$', exp_score_delete, name='exp_score_delete'),

    url(r'^exp_list_undo/$',exp_list_undo,name='exp_list_undo'),
    url(r'^exp_list_doing/$', exp_list_doing, name='exp_list_doing'),
    url(r'^exp_list_done/$', exp_list_done, name='exp_list_done'),
    url(r'^exp_list_scored/$', exp_list_scored, name='exp_list_scored'),

    url(r'^exp_instance_start/(\d+)/$', exp_instance_start, name='exp_instance_start'),

    #repo operate
    url(r'^repo_home/$',repo_home,name='repo_home'),
    url(r'^repo_public_list/$',repo_home,name='repo_home'),
    url(r'^repo_public_image_list/$', repo_public_image_list, name='repo_public_image_list'),
    url(r'^repo_private_exp_list/$',repo_private_exp_list,name='repo_private_exp_list'),
    url(r'^repo_private_image_list/$',repo_private_image_list,name='repo_private_image_list'),
    url(r'^repo_private_network_list/$',repo_private_network_list,name='repo_private_network_list'),
    url(r'^repo_private_VM_list/$', repo_private_VM_list, name='repo_private_VM_list'),
    url(r'^repo_create_image/$',repo_create_image,name='repo_create_image'),
    url(r'^repo_create_network/$', repo_create_network, name='repo_create_network'),


    url(r'^repo_public_exp_delete/(\d+)$',repo_public_exp_delete,name='repo_public_exp_delete'),
    url(r'^repo_public_image_delete/(\d+)$',repo_public_image_delete,name='repo_public_image_delete'),
    url(r'^repo_image_detail/(\d+)$',repo_image_detail,name='repo_image_detail'),
    url(r'^repo_image_edit/(\d+)$',repo_image_edit,name='repo_image_edit'),
    url(r'^repo_image_delete/(\d+)$',repo_image_delete,name='repo_image_delete'),
    url(r'^repo_image_share/(\d+)$', repo_image_share, name='repo_image_share'),
    url(r'^repo_network_detail/(\d+)$', repo_network_detail, name='repo_network_detail'),
    url(r'^repo_network_edit/(\d+)$', repo_network_edit, name='repo_network_edit'),
    url(r'^repo_network_delete/(\d+)$', repo_network_delete, name='repo_network_delete'),
    url(r'^repo_VM_detail/(\d+)$', repo_VM_detail, name='repo_VM_detail'),
    url(r'^repo_VM_edit/(\d+)$', repo_VM_edit, name='repo_VM_edit'),
    url(r'^repo_VM_delete/(\d+)$', repo_VM_delete, name='repo_VM_delete'),


    url(r'^repo_ImageCart_list/$',repo_ImageCart_list,name='repo_ImageCart_list'),
    url(r'^repo_ImageCart_clear/$',repo_ImageCart_clear,name='repo_ImageCart_clear'),
    url(r'^repo_ImageCart_add(\d+)/$', repo_ImageCart_add, name='repo_ImageCart_add'),
    url(r'^repo_ImageCart_delete/(\d+)$', repo_ImageCart_delete, name='repo_ImageCart_delete'),
    url(r'^repo_NetworkCart_list/$',repo_NetworkCart_list,name='repo_NetworkCart_list'),
    url(r'^repo_NetworkCart_clear/$',repo_NetworkCart_clear,name='repo_NetworkCart_clear'),
    url(r'^repo_NetworkCart_add/(\d+)$', repo_NetworkCart_add, name='repo_NetworkCart_add'),
    url(r'^repo_NetworkCart_delete/(\d+)$', repo_NetworkCart_delete, name='repo_NetworkCart_delete'),


    #teaching statistic
    url(r'^teach_home/$',teach_home,name='teach_home'),
    url(r'^teach_result_list/$',teach_result_list,name='teach_result_list'),#show all situation=done data from score db
    url(r'^teach_score_list/$', teach_score_list, name='teach_score_list'),
    url(r'^teach_score_list_by_stu/$', teach_score_list_by_stu, name='teach_score_list_by_stu'),
    url(r'^teach_situation_detail_by_delivery(\d+)/$',teach_situation_detail_by_delivery,name='teach_situation_detail_by_delivery'),
    url(r'^teach_situation_detail_by_scoreID(\d+)/$',teach_situation_detail_by_scoreID,name='teach_situation_detail_by_scoreID'),
    # url(r'^teach_result_list_by_delivery(\d+)/$',teach_result_list_by_delivery,name='teach_result_list_by_delivery'),
    url(r'^teach_score_list_by_deliveryID(\d+)/$',teach_score_list_by_deliveryID,name='teach_score_list_by_deliveryID'),
    url(r'^teach_score_list_by_stuID(\d+)/$', teach_score_list_by_stuID, name='teach_score_list_by_stuID'),
    url(r'^teach_score_list_by_expID(\d+)/$', teach_score_list_by_expID, name='teach_score_list_by_expID'),
    # url(r'^teach_score_list_by_scoreID(\d+)/$',teach_score_list_by_scoreID,name='teach_score_list_by_scoreID'),
    url(r'^teach_result_score(\d+)/$',teach_result_score,name='teach_result_score'),
    url(r'^teach_result_report_download(\d+)/$',teach_result_report_download,name='teach_result_report_download'),
    url(r'^teach_score_list_by_group/$', teach_score_list_by_group, name='teach_score_list_by_group'),
    url(r'^teach_score_list_by_groupID(\d+)/$', teach_score_list_by_groupID, name='teach_score_list_by_groupID'),

    #delivery operate
    url(r'^delivery_list/$',delivery_list,name='delivery_list'),
    url(r'^delivery_detail/(\d+)/$',delivery_detail,name='delivery_detail'),
    url(r'^delivery_edit/(\d+)/$', delivery_edit, name='delivery_edit'),
    url(r'^delivery_delete/(\d+)/$', delivery_delete, name='delivery_delete'),
    url(r'^delivery_create/$', delivery_create, name='delivery_create'),


]
