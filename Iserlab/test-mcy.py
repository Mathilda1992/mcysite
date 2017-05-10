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


def vm_instance_save(request,vi_id):#save as a VM template
    try:
        vi = VMInstance.objects.get(id=vi_id)
    except VMInstance.DoesNotExist:
        raise Http404
    #first check if the VMInstance slready has a snapshot by check the "result_image" field
    if vi.result_image:
        try:
            snapshot_image = VMImage.objects.get(id=vi.result_image)
        except VMImage.DoesNotExist:
            raise Http404
        username = request.session['username']
        role = request.session['role']

        if request.method == 'POST':
            rf = SaveVMasTemplate(request.POST)
            if rf.is_valid():
                name = rf.cleaned_data['name']
                desc = rf.cleaned_data['desc']

                # step1:get necessary data from VMInstance
                network = vi.connect_net.network
                flavor = vi.vm.flavor
                keypair = vi.vm.keypair
                security_group = vi.vm.security_group

                # step2:insert a new record into VM
                new_vm = VM(name=name,desc=desc,owner_name=username,image=snapshot_image,network=network,flavor=flavor,keypair=keypair,security_group=security_group)
                new_vm.save()
                return HttpResponseRedirect('/repo_private_VM_list/')
        else:
            rf = SaveVMasTemplate()
        return render(request, "vm_instance_save.html", {'rf': rf})
    else:
        return HttpResponse("please first make a snapshot for the VM Instance.")



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



#only role=stu has this operation
def exp_submit(request,d_id):#??
    username = request.session['username']
    role = request.session['role']
    if role=="teacher":
        return HttpResponse("Teacher do not have this function")
    else:
        s = Student.objects.get(stu_username=username)
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
            e = Experiment(exp_name=name,exp_description=desc,exp_owner_name=username,exp_image_count=len(imageList),VM_count=e.VM_count,operate_vm_id=e.operate_vm_id)
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
