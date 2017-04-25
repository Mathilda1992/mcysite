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
            vm = VM(name=name,desc=desc,owner_name=username,exp=e,image=image,network=net,flavor=flavor,keypair=keypair,security_group=security_group)
            vm.save()
            #update the VM_count of Experiment
            re = Experiment.objects.filter(id=exp_id).update(VM_count=e.VM_count+1)
            return HttpResponseRedirect('/exp_home/')
    else:
        rf = AddVMForm()
    return render_to_response("exp_create_VM.html",{'rf':rf})




#only role = teacher has this function
def exp_edit(request,exp_id):
    try:
        e = Experiment.objects.get(id=exp_id)
    except Experiment.DoesNotExist:
        raise Http404
    imageList = e.exp_images.all()
    networkList = e.exp_network.all()
    images_idList=[]#should be ImageCart id
    networks_idList=[]#should be NetworkCart id
    for item in imageList:
        image_in_cart = ImageCart.objects.get(image=item)
        images_idList.append(image_in_cart.id)
    for item in networkList:
        network_in_cart = NetworkCart.objects.get(network=item)
        networks_idList.append(network_in_cart.id)

    #edit and update the exp
    if request.method == 'POST':
        rf = EditExpForm(request.POST)
        if rf.is_valid():
            #get input data from form
            update_name = rf.cleaned_data['name']
            update_desc = rf.cleaned_data['desc']
            update_images_idList = rf.cleaned_data['images_idList']#this id is ImageCart id
            update_networks_idList = rf.cleaned_data['networks_idList']#this id is NetworkCart id
            update_vm_count = rf.cleaned_data['vm_count']
            # update_guide = rf.data['guide']
            # update_refer_result = rf.data['refer_result']
            print "after update"
            print update_images_idList
            update_imageList =[]
            update_networkList=[]
            for i in update_images_idList:
                image_in_cart = ImageCart.objects.get(id=i)
                update_imageList.append(VMImage.objects.get(id=image_in_cart.image.id))
            for i in update_networks_idList:
                network_in_cart = NetworkCart.objects.get(id=i)
                update_networkList.append(Network.objects.get(id=network_in_cart.network.id))

            #update basic info for exp
            re = Experiment.objects.filter(id=exp_id).update(exp_name=update_name,exp_description=update_desc,
                                                             exp_image_count=len(update_imageList),
                                                             exp_updatetime=datetime.datetime.now(),
                                                             VM_count=update_vm_count)
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
        attrs['vm_count'] = e.VM_count
        gf = EditExpForm(initial=attrs)
    return render_to_response("exp_edit.html",{'rf':gf})