#mcy update in 2016-12-20
#Make Experiment as a kind of resource like image,VM,network, and below give some related operations

from Iserlab import image_resource_operation,compute_resource_operation,network_resource_operation
from Iserlab.models import Experiment,VMInstance,ExpInstance,User,Student,Group,VMImage,Network,Delivery

#---------attrs for exp object--------
#['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', u'__module__', '__ne__',
# '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_base_manager',
# '_check_column_name_clashes', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_local_fields', '_check_long_column_names',
# '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_ordering', '_check_swappable', '_check_unique_together', '_default_manager', '_deferred',
# '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks',
# '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'delivery_set', 'exp_createtime',
# 'exp_description', 'exp_guide', 'exp_image_count', 'exp_images', 'exp_name', 'exp_network', 'exp_owner', 'exp_owner_id', 'exp_reportDIR', 'exp_result', 'exp_updatetime', 'expinstance_set',
# 'from_db', 'full_clean', 'get_deferred_fields', 'get_next_by_exp_createtime', 'get_next_by_exp_updatetime', 'get_previous_by_exp_createtime', 'get_previous_by_exp_updatetime', 'id',
# 'is_shared', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'shared_time', 'unique_error_message', 'validate_unique']





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Get current user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def get_currentuser(name):
    print('Get current User:')
    print User.objects.get(username = name)
    return User.objects.get(username = name)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Get experiment (ManyToMany) attribute~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def get_expVMImage(experiment_id):
    print('Get the VMImages of exp:')
    imagelist = []
    e = Experiment.objects.get(id = experiment_id)
    imagelist = e.exp_images.all()
    return imagelist

def get_expNetwork(experiment_id):
    print('Get the network of the exp:')
    e = Experiment.objects.get(id=experiment_id)
    networklist = e.exp_network.all()
    return networklist


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~List experiment template~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def list_experiment():
    print("List Experiments:")
    Experiment_list = Experiment.objects.all()
    #return data****
    # [<Experiment: id=2,name=exp000>, <Experiment: id=1,name=exptest1>]

    for exp in Experiment_list:
        print exp
    return Experiment_list



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Filter experiment template by condition~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def filter_experiment_by_user(name):
    currentuser = User.objects.get(username = name)
    elist = Experiment.objects.filter(exp_owner = currentuser)
    return elist


def filter_experiment_by_shared():
    elist = Experiment.objects.filter(is_shared = True)
    return elist


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~View experiment template detail~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def view_experiment_detail(experiment_id):
    e =  Experiment.objects.get(id = experiment_id)
    #analyse the info into a dict
    edict={'id':experiment_id}
    ##edict={}.fromkeys('id','name','owner','imageCount','imagelist','network','is_shared','description')
    edict['exp_name'] = e.exp_name
    edict['exp_owner'] = e.exp_owner
    edict['exp_createtime']=e.exp_createtime
    edict['exp_updatetime']=e.exp_updatetime
    edict['exp_image_count'] = e.exp_image_count
    imagelist = e.exp_images.all()
    edict['exp_images'] = imagelist
    network = e.exp_network.all()
    edict['exp_network'] = network
    edict['is_shared'] = e.is_shared
    edict['shared_time'] = e.shared_time
    deliverys = Delivery.objects.filter(exp=e, teacher=e.exp_owner).order_by('-delivery_time')
    edict['delivery_history'] = deliverys
    edict['exp_description'] = e.exp_description
    edict['exp_guide'] = e.exp_guide
    edict['exp_result'] =e.exp_result
    edict['exp_reportDIR']=e.exp_reportDIR

    # print edict
    # for key,value in edict.items():
    #     print 'key=%s,value=%s' % (key,value)
    return edict




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create experiment~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Copy experiment template~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#when teacher directly use exp template in repo, it copy one
def copy_experiment(experiment_id,current_username):
    #get source exp template from db
    source_e = Experiment.objects.get(id = experiment_id)

    print"*****"
    print type(source_e.id)
    print source_e.exp_name
    print source_e.exp_description
    print source_e.exp_image_count
    print type(source_e.exp_image_count)

    #get attributes of source exp
    new_name = 'copy of exp'
    new_owner = User.objects.get(username = current_username)
    new_is_shared = False

    imagelist = []
    imagelist = source_e.exp_images.all()
    imagecount = len(imagelist)
    networklist = []
    networklist = source_e.exp_network.all()
    desc = source_e.exp_description
    guide = source_e.exp_guide
    result = source_e.exp_result
    reportDIR = source_e.exp_reportDIR


    #create a copy one
    copied_e = create_experiment(new_name, new_owner,imagelist,imagecount,networklist,new_is_shared,desc,guide,result,reportDIR)

    return copied_e



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Modify experiment template~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Only who create the exp_template can Modify it
def modify_experiment(experiment_id,name,description,imageList,network_name,guide,result,reportDIR,updatetime):
    print ('Modify Experiment: ')
    #get modified input from html page
    #********************

    #modify fields in db table:Experiment
    #********************
    Experiment.objects.filter(id = experiment_id).update(
        exp_name = name,
        exp_description = description,
        exp_images = imageList,
        exp_network = network_name,
        exp_guide = guide,
        exp_result =result,
        exp_reportDIR = reportDIR,
        exp_updatetime = updatetime
    )

    #return the modified exp
    modified_exp = Experiment.objects.get(id = experiment_id)

    return modified_exp





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delete experiment template~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Only who create the exp_template can delete it
def delete_experiment(experiment_id):
    print ('Delete Experiment: ')
    e = Experiment.objects.get(id = experiment_id)
    e.delete()
    pass





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prepare experiment image~~~~~~~~~~~~~~~~~~~~~~~#
def add_image_cart(image_name):
    #insert a new record into db
    pass

def list_image_cart():
    #Get all records from db
    pass

def delete_image_cart(image_name):
    #delete the record in db
    pass

def find_image_cart(image_name):
    pass



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prepare experiment Network~~~~~~~~~~~~~~~~~~~~~~~#
def add_network_cart():
    pass

def list_network_cart():
    pass

def modify_network_cart():
    pass

def delete_network_cart():
    pass









#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Launch experiment instance~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
##step1:check whether the network instance running, created one if does not exist,else return the network id
def luanch_exp_network(conn,e_id):
    print ("Launch Exp Network: ")
    e = Experiment.objects.get(exp_name=e_id)

    # get the network info of exp
    nlist = []
    nlist = e.exp_network.all()
    # nlist = Network.objects.filter(id=n_id)
    print nlist
    n_id_list = []
    n_name_list = []
    sn_name_list = []
    ip_version_list = []
    cidr_list = []
    gateway_ip_list = []
    description_list = []
    owner_list = []
    is_shared_list = []
    for n in nlist:
        n_id_list.append(n.network_id)
        n_name_list.append(n.network_name)
        sn_name_list.append(n.subnet_name)
        ip_version_list.append(n.ip_version)
        cidr_list.append(n.cidr)
        gateway_ip_list.append(n.gateway_ip)
        description_list.append(n.network_description)
        owner_list.append(n.owner)
        is_shared_list.append(n.is_shared)


    existing_n_list = network_resource_operation.list_networks(conn)
    #extract the network info into a [dict] list


    # check whether the network instance exists? if not, Create network instance
    for i in range(0,len(nlist)):

        if re:
            pass
        else:
            n_cidr=network_resource_operation.create_network(conn, n_name_list[i], sn_name_list[i], ip_version_list[i],
                                                      cidr_list[i], gateway_ip_list[i],description_list[i],owner_list[i],is_shared_list[i])
    print '###################finished launch network########'
    print n_cidr



    return 0


##step2:get the image info the exp contians, create vms based on these images

def launch_experiment_instance(conn,e_id):
    print ("Launch Experiment: ")
    #Get the exp object from db by given exp_name
    e = Experiment.objects.get(exp_name = e_id)


    #geth the image info
    ilist = []
    ilist = e.exp_images.all()
    image_id_list = []
    flavor_name_list = []
    private_keypair_name_list =[]
    for i in ilist:
        image_id_list.append(i.image_id)
        flavor_name_list.append(i.flavor)
        private_keypair_name_list.append(i.keypair)

    #create VM instance
    serverList = []
    for i in len(ilist):
        server_name = 'server' + i
        image_id = image_id_list[i]
        flavor_name = flavor_name_list[i]
        network_id = n_id_list[0]
        private_keypair_name = private_keypair_name_list[i]
        server = compute_resource_operation.create_server3(conn,server_name,image_id,flavor_name,network_id,private_keypair_name)
        serverList.append(server)

    #convert the servers info into a Dict_List
    #********************
    serverDictList = []
    serverIDList = []

    #insert all servers into db:VMInstance
    for serverDict in serverDictList:
        VMInstance.objects.create(
            id = serverDict.id,
            name = serverDict.name,
            owner = serverDict.owner,
            createtime = serverDict.created,
            updatetime = serverDict.updated,
            status = serverDict.status,
            ip = serverDict.accessIPv4
        )


    #store the exp instance info in a Dict var
    #***************
    expInstanceDict={}

    #Insert a exp instance record into db:ExpInstance
    #***************
    # ExpInstance.objects.create(
    #     name = experiment_name
    # )
    return expInstanceDict


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Modify experiment instance~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def modify_experiment_instance():
    pass



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Save experiment as template~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def save_experiment(conn):
    pass



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delivery experiment to student~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def delivery_experiment(conn,e_id,stu_list):
    pass