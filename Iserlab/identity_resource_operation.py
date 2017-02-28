#mcy update 2016-12-05
#Refer to:http://developer.openstack.org/sdks/python/openstacksdk/users/proxies/identity.html#identity-api-v3
##https://developer.openstack.org/sdks/python/openstacksdk/users/proxies/identity_v3.html
#operation on openstack identity resources

#/*****************************************User Operations***********************************/
def extract_user(users):
    list = []
    for item in users:
        print item
        dict = {}
        dict.setdefault("allow_create ",item.allow_create )
        dict.setdefault("allow_delete ", item.allow_delete)
        dict.setdefault("allow_get ", item.allow_get)
        dict.setdefault("allow_head ", item.allow_head)
        dict.setdefault("allow_list ", item.allow_list)
        dict.setdefault("allow_update ", item.allow_update)
        dict.setdefault("base_path ", item.base_path)
        dict.setdefault("create ", item.create)
        dict.setdefault("default_project_id ", item.default_project_id)
        dict.setdefault("delete ", item.delete)
        dict.setdefault("description ", item.description)
        dict.setdefault("domain_id ", item.domain_id)#
        dict.setdefault("email ", item.email)
        dict.setdefault("existing ", item.existing)
        dict.setdefault("find ", item.find)
        dict.setdefault("get ", item.get)
        dict.setdefault("head ", item.head)
        dict.setdefault("id", item.id)#
        dict.setdefault("is_enabled", item.is_enabled)#
        dict.setdefault("links ", item.links)#
        dict.setdefault("list ", item.list)
        dict.setdefault("location ", item.location)
        dict.setdefault("name", item.name)#
        dict.setdefault("new ", item.new)
        dict.setdefault("password ", item.password)
        dict.setdefault("password_expires_at ", item.password_expires_at)
        dict.setdefault("patch_update ", item.patch_update)
        dict.setdefault("put_create ", item.put_create)
        dict.setdefault("resource_key ", item.resource_key)
        dict.setdefault("resources_key ", item.resources_key)
        dict.setdefault("service ", item.service)
        # dict.setdefault("to_dict ", item.to_dict)
        dict.setdefault("update ", item.update)
        list.append(dict)
    print "the data after extract"
    for i in list:
        print i
    return list
#--------------------all attrs of user to access-------------------------------------
# ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
# '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_alternate_id', '_body', '_body_mapping', '_collect_attrs', '_consume_attrs', '_filter_component', '_get_id',
# '_get_mapping', '_get_one_match', '_header', '_header_mapping', '_prepare_request', '_query_mapping', '_translate_response', '_update', '_uri', '_uri_mapping', 'allow_create', 'allow_delete',
# 'allow_get', 'allow_head', 'allow_list', 'allow_update', 'base_path', 'create', 'default_project_id', 'delete', 'description', 'domain_id', 'email', 'existing', 'find', 'get', 'head', 'id',
#  'is_enabled', 'links', 'list', 'location', 'name', 'new', 'password', 'password_expires_at', 'patch_update', 'put_create', 'resource_key', 'resources_key', 'service', 'to_dict', 'update']



def list_users(conn):
    print("List openstack Users:")
    users = conn.identity.users()
    return extract_user(users)
#data before extract
#openstack.identity.v3.user.User(id=03e0e7f58179416a8fdd582924bf9283, enabled=True, name=lyj, links={u'self': u'http://controller:5000/v3/users/03e0e7f58179416a8fdd582924bf9283'}, domain_id=default)
#openstack.identity.v3.user.User(id=1c10eeae495e4b059ad9adbd9f8f98f3, enabled=True, name=glance, links={u'self': u'http://controller:5000/v3/users/1c10eeae495e4b059ad9adbd9f8f98f3'}, domain_id=default)



def create_user(conn):
    print("Create openstack User")
    pass

def delete_user(conn):
    pass


def update_user(conn):
    pass

#***************************Project Operations***************************************
def extract_project(projects):
    list = []
    for item in projects:
        print item
        dict = {}
        dict.setdefault("allow_create ", item.allow_create)
        dict.setdefault("allow_delete ", item.allow_delete)
        dict.setdefault("allow_get ", item.allow_get)
        dict.setdefault("allow_head ", item.allow_head)
        dict.setdefault("allow_list ", item.allow_list)
        dict.setdefault("allow_update ", item.allow_update)
        dict.setdefault("base_path ", item.base_path)
        dict.setdefault("create ", item.create)
        dict.setdefault("delete ", item.delete)
        dict.setdefault("description ", item.description)
        dict.setdefault("domain_id ", item.domain_id)  #
        dict.setdefault("existing ", item.existing)
        dict.setdefault("find ", item.find)
        dict.setdefault("get ", item.get)
        dict.setdefault("head ", item.head)
        dict.setdefault("id", item.id)  #
        dict.setdefault("is_domain",item.is_domain)
        dict.setdefault("is_enabled", item.is_enabled)  #
        dict.setdefault("list ", item.list)
        dict.setdefault("location ", item.location)
        dict.setdefault("name", item.name)  #
        dict.setdefault("new ", item.new)
        dict.setdefault("parent_id", item.parent_id)
        dict.setdefault("patch_update ", item.patch_update)
        dict.setdefault("put_create ", item.put_create)
        dict.setdefault("resource_key ", item.resource_key)
        dict.setdefault("resources_key ", item.resources_key)
        dict.setdefault("service ", item.service)
        # dict.setdefault("to_dict ", item.to_dict)
        dict.setdefault("update ", item.update)
        list.append(dict)

    for i in list:
        print i
    return list
#--------------------all attrs of project to access-------------------------------------
#['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__',
# '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_alternate_id', '_body', '_body_mapping', '_collect_attrs', '_consume_attrs', '_filter_component',
# '_get_id', '_get_mapping', '_get_one_match', '_header', '_header_mapping', '_prepare_request', '_query_mapping', '_translate_response', '_update', '_uri', '_uri_mapping', 'allow_create',
# 'allow_delete', 'allow_get', 'allow_head', 'allow_list', 'allow_update', 'base_path', 'create', 'delete', 'description', 'domain_id', 'existing', 'find', 'get', 'head', 'id', 'is_domain',
# 'is_enabled', 'list', 'location', 'name', 'new', 'parent_id', 'patch_update', 'put_create', 'resource_key', 'resources_key', 'service', 'to_dict', 'update']



def list_projects(conn):
    print("List openstack Projects:")
    projects = conn.identity.projects()
    return extract_project(projects)

#List Projects:
#openstack.identity.v3.project.Project(is_domain=False, description=QuLeilei Project, enabled=True, domain_id=default, parent_id=None, id=02d5ad020bec441185dd901f61cb28db, name=quleilei)
#openstack.identity.v3.project.Project(is_domain=False, description=Liuying Project, enabled=True, domain_id=default, parent_id=None, id=1b136c88aa6f4b8ebfd7ab9803c938c5, name=liuying)



def create_project(conn,**new_project_attrs):
    print new_project_attrs



def delete_project(conn):
    pass


def get_project(conn,project):
    pass


def find_project(conn,id_or_name):
    project = conn.identity.find_project(id_or_name)
    print project
    return project


def update_project(conn,project,**attrs):
    pass


#/*****************************************domain Operations***********************************/
def list_domains(conn):
    print("List openstack Domains:")

    for domain in conn.identity.domains():
        print(domain)
        print dir(domain)
    return conn.identity.domains()





#/*****************************************Role Operations***********************************/

def list_roles(conn):
    roles = conn.identity.roles()#!!!!!!!ERROR:AttributeError: 'Proxy' object has no attribute 'roles'
    for item in roles:
        print item

    pass

def create_role(conn):
    dict={}
    dict.setdefault("rolename",'user')
    print dict
    new = conn.identity.create_role(**dict)

    pass

def get_role(conn,role):
    pass

def find_role(conn,name_or_id):
    pass

def list_role_assigns(conn):
    role_assigns = conn.identity.role_assignments()
    for item in role_assigns:
        print item

#/*****************************************other Operations***********************************/
def list_groups(conn):
    print("List Groups:")

    for group in conn.identity.groups():
        print(group)


def list_services(conn):
    print("List Services:")

    for service in conn.identity.services():
        print(service)


def list_endpoints(conn):
    print("List Endpoints:")

    for endpoint in conn.identity.endpoints():
        print(endpoint)


def list_regions(conn):
    print("List Regions:")

    for region in conn.identity.regions():
        print(region)


def list_credentials(conn):
    print("List Credentials:")

    for credential in conn.identity.credentials():
        print(credential)
    return conn.identity.credentials()
