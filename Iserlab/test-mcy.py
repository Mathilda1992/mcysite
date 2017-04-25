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
    router_dict = network_resource_operation.remove_interface_from_router(conn, r, subnet_id)
    print router_dict
    return HttpResponse('remove interface from Router')



class AddExpForm(forms.Form):
    name = forms.CharField(label='Exp Name',max_length=150)
    desc = forms.CharField(label='Description',max_length=500,
                           widget=forms.Textarea(),
                           required =False)

    images_idList = forms.MultipleChoiceField(label='Include Images',
                                       widget=forms.CheckboxSelectMultiple,
                                       )
    networks_idList = forms.MultipleChoiceField(label='Use Networks',
                                         widget=forms.CheckboxSelectMultiple,
                                         )
    vm_count = forms.IntegerField(label="VM Count")
    # vm_idList = forms.MultipleChoiceField(label='Include VMs',)

    guide_file = forms.FileField(label='Upload Guide File', required=True)


    def __init__(self,*args,**kwargs):
        super(AddExpForm,self).__init__(*args,**kwargs)
        self.fields['images_idList'].choices = [(i.pk,str(i)) for i in ImageCart.objects.all()]
        self.fields['networks_idList'].choices = [(i.pk,str(i)) for i in NetworkCart.objects.all()]


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