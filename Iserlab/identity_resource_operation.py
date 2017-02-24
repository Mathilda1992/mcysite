#mcy update 2016-12-05
#Refer to:http://developer.openstack.org/sdks/python/openstacksdk/users/proxies/identity.html#identity-api-v3
##https://developer.openstack.org/sdks/python/openstacksdk/users/proxies/identity_v3.html
#operation on openstack identity resources

#/*****************************************User Operations***********************************/
def list_users(conn):
    print("List openstack Users:")
    users = conn.identity.users()

    list = []
    for item in users:
        print item
        # print item.links['self']
        #extract data
        dict = {}
        dict.setdefault("id",item.id)
        # dict.setdefault("enabled",item.enabled);
        dict.setdefault("name",item.name)
        dict.setdefault("links",item.links['self'])
        dict.setdefault("domain_id",item.domain_id)
        list.append(dict)

    print "the data after extract"
    for i in list:
        print i
    return list
#data before extract
#openstack.identity.v3.user.User(id=03e0e7f58179416a8fdd582924bf9283, enabled=True, name=lyj, links={u'self': u'http://controller:5000/v3/users/03e0e7f58179416a8fdd582924bf9283'}, domain_id=default)
#openstack.identity.v3.user.User(id=1c10eeae495e4b059ad9adbd9f8f98f3, enabled=True, name=glance, links={u'self': u'http://controller:5000/v3/users/1c10eeae495e4b059ad9adbd9f8f98f3'}, domain_id=default)
#openstack.identity.v3.user.User(id=1dfb08cb0f4747f58e34e2bc02ee3d92, enabled=True, name=teacher, links={u'self': u'http://controller:5000/v3/users/1dfb08cb0f4747f58e34e2bc02ee3d92'}, domain_id=default)
#openstack.identity.v3.user.User(id=36efd260c02b42d1968fc20db1477f34, enabled=True, name=neutron, links={u'self': u'http://controller:5000/v3/users/36efd260c02b42d1968fc20db1477f34'}, domain_id=default)
#openstack.identity.v3.user.User(id=424cb1c3e87d4358bbef741e6253c62b, enabled=True, name=quleilei, links={u'self': u'http://controller:5000/v3/users/424cb1c3e87d4358bbef741e6253c62b'}, domain_id=default)
#openstack.identity.v3.user.User(id=428c18c9f6a34f9c9a222cc4226d0dad, enabled=True, name=qinli, links={u'self': u'http://controller:5000/v3/users/428c18c9f6a34f9c9a222cc4226d0dad'}, domain_id=default)
#openstack.identity.v3.user.User(id=48476c83c1634f9d8cba95b1381d8e58, enabled=True, name=admin, links={u'self': u'http://controller:5000/v3/users/48476c83c1634f9d8cba95b1381d8e58'}, domain_id=default)
#openstack.identity.v3.user.User(id=5758e584a8b543c784aaaa007f1a8ff6, enabled=True, name=liuying, links={u'self': u'http://controller:5000/v3/users/5758e584a8b543c784aaaa007f1a8ff6'}, domain_id=default)
#openstack.identity.v3.user.User(id=8903fd567f124fc2911079499a8d0c50, enabled=True, name=demo, links={u'self': u'http://controller:5000/v3/users/8903fd567f124fc2911079499a8d0c50'}, domain_id=default)
#openstack.identity.v3.user.User(id=a09196e34875467c9d2ac2a4f2514421, enabled=True, name=mcy, links={u'self': u'http://controller:5000/v3/users/a09196e34875467c9d2ac2a4f2514421'}, domain_id=default)
#openstack.identity.v3.user.User(id=ad01cdcecfb345b7ac8dcb73e436f051, enabled=True, name=cinder, links={u'self': u'http://controller:5000/v3/users/ad01cdcecfb345b7ac8dcb73e436f051'}, domain_id=default)
#openstack.identity.v3.user.User(id=e576f8e3066a4adfa93f1e7b3d9ccd5e, enabled=True, name=nova, links={u'self': u'http://controller:5000/v3/users/e576f8e3066a4adfa93f1e7b3d9ccd5e'}, domain_id=default)

#the data after extract
#{'domain_id': u'default', 'id': u'03e0e7f58179416a8fdd582924bf9283', 'links': u'http://controller:5000/v3/users/03e0e7f58179416a8fdd582924bf9283', 'name': u'lyj'}
#{'domain_id': u'default', 'id': u'1c10eeae495e4b059ad9adbd9f8f98f3', 'links': u'http://controller:5000/v3/users/1c10eeae495e4b059ad9adbd9f8f98f3', 'name': u'glance'}
#{'domain_id': u'default', 'id': u'1dfb08cb0f4747f58e34e2bc02ee3d92', 'links': u'http://controller:5000/v3/users/1dfb08cb0f4747f58e34e2bc02ee3d92', 'name': u'teacher'}
#{'domain_id': u'default', 'id': u'36efd260c02b42d1968fc20db1477f34', 'links': u'http://controller:5000/v3/users/36efd260c02b42d1968fc20db1477f34', 'name': u'neutron'}
#{'domain_id': u'default', 'id': u'424cb1c3e87d4358bbef741e6253c62b', 'links': u'http://controller:5000/v3/users/424cb1c3e87d4358bbef741e6253c62b', 'name': u'quleilei'}
#{'domain_id': u'default', 'id': u'428c18c9f6a34f9c9a222cc4226d0dad', 'links': u'http://controller:5000/v3/users/428c18c9f6a34f9c9a222cc4226d0dad', 'name': u'qinli'}
#{'domain_id': u'default', 'id': u'48476c83c1634f9d8cba95b1381d8e58', 'links': u'http://controller:5000/v3/users/48476c83c1634f9d8cba95b1381d8e58', 'name': u'admin'}
#{'domain_id': u'default', 'id': u'5758e584a8b543c784aaaa007f1a8ff6', 'links': u'http://controller:5000/v3/users/5758e584a8b543c784aaaa007f1a8ff6', 'name': u'liuying'}
#{'domain_id': u'default', 'id': u'8903fd567f124fc2911079499a8d0c50', 'links': u'http://controller:5000/v3/users/8903fd567f124fc2911079499a8d0c50', 'name': u'demo'}
#{'domain_id': u'default', 'id': u'a09196e34875467c9d2ac2a4f2514421', 'links': u'http://controller:5000/v3/users/a09196e34875467c9d2ac2a4f2514421', 'name': u'mcy'}
#{'domain_id': u'default', 'id': u'ad01cdcecfb345b7ac8dcb73e436f051', 'links': u'http://controller:5000/v3/users/ad01cdcecfb345b7ac8dcb73e436f051', 'name': u'cinder'}
#{'domain_id': u'default', 'id': u'e576f8e3066a4adfa93f1e7b3d9ccd5e', 'links': u'http://controller:5000/v3/users/e576f8e3066a4adfa93f1e7b3d9ccd5e', 'name': u'nova'}

def create_user(conn):
    print("Create openstack User")
    pass

def delete_user(conn):
    pass


def update_user(conn):
    pass

#***************************Project Operations***************************************
def list_projects(conn):
    print("List openstack Projects:")
    projects = conn.identity.projects()

    list = []
    for item in projects:
        print item
        # extract data
        dict = {}
        dict.setdefault("id_domain", item.is_domain)
        dict.setdefault("description",item.description)
        # dict.setdefault("enabled", item.enabled)
        dict.setdefault("domain_id", item.domain_id)
        dict.setdefault("parent_id",item.parent_id)
        dict.setdefault("id", item.id)
        dict.setdefault("name", item.name)
        list.append(dict)

    for i in list:
        print i
    return list
#List Projects:
#openstack.identity.v3.project.Project(is_domain=False, description=QuLeilei Project, enabled=True, domain_id=default, parent_id=None, id=02d5ad020bec441185dd901f61cb28db, name=quleilei)
#openstack.identity.v3.project.Project(is_domain=False, description=Liuying Project, enabled=True, domain_id=default, parent_id=None, id=1b136c88aa6f4b8ebfd7ab9803c938c5, name=liuying)
#openstack.identity.v3.project.Project(is_domain=False, description=Admin Project create on 2016-11-15, enabled=True, domain_id=default, parent_id=None, id=2f1bc8c34f094d049a201819732537a3, name=admin)
#openstack.identity.v3.project.Project(is_domain=False, description=Qinli Project, enabled=True, domain_id=default, parent_id=None, id=388abc648a20494eba70dab8ccfa9d14, name=qinli)
#openstack.identity.v3.project.Project(is_domain=False, description=Service Project create on 2016-11-15, enabled=True, domain_id=default, parent_id=None, id=6266384750f949148eebf160fadcd662, name=service)
#openstack.identity.v3.project.Project(is_domain=False, description=Demo Project create on 2016-11-15, enabled=True, domain_id=default, parent_id=None, id=7ad82b22a6924a978c54862efb3517f2, name=demo)
#openstack.identity.v3.project.Project(is_domain=False, description=lyj Project-comman, enabled=True, domain_id=default, parent_id=None, id=7f4cc78a61d0484d8cc57441c0857f6a, name=lyj)
#openstack.identity.v3.project.Project(is_domain=False, description=teacher Project, enabled=True, domain_id=default, parent_id=None, id=bd9dc26b524143339cad03c0ee048429, name=teacher)
#openstack.identity.v3.project.Project(is_domain=False, description=Machenyi Project, enabled=True, domain_id=default, parent_id=None, id=f9085a59e485496eb44dce5608d438d1, name=mcy)

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
