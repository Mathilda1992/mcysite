#mcy update in 2016-12-07
##refer to : http://developer.openstack.org/sdks/python/openstacksdk/users/proxies/compute.html

#content:
# List Servers
# List Images
# List Flavors
# List Networks
# Create Key Pair
# Create Server
#......

import os

def extract_server(servers):
    list =[]
    for item in servers:
        # print(dir(item))
        dict ={}
        print item.to_dict
        dict.setdefault("access_ipv4",item.access_ipv4)#
        dict.setdefault("access_ipv6",item.access_ipv6)#
        dict.setdefault("add_security_group",item.add_security_group)
        dict.setdefault("addresses", item.addresses)#
        dict.setdefault("admin_password", item.admin_password)
        dict.setdefault("allow_create",item.allow_create)
        dict.setdefault("allow_delete",item.allow_delete)
        dict.setdefault("allow_get",item.allow_get)
        dict.setdefault("allow_head",item.allow_head)
        dict.setdefault("allow_list",item.allow_list)
        dict.setdefault("allow_update",item.allow_update)
        dict.setdefault("attached_volumes",item.attached_volumes)
        dict.setdefault("availability_zone",item.availability_zone)
        dict.setdefault("base_path",item.base_path)
        dict.setdefault("block_device_mapping",item.block_device_mapping)
        dict.setdefault("change_password",item.change_password)
        dict.setdefault("confirm_resize",item.confirm_resize)
        dict.setdefault("create", item.create)
        dict.setdefault("create_image", item.create_image)
        dict.setdefault("created_at",item.created_at)#
        dict.setdefault("delete",item.delete)
        dict.setdefault("delete_metadata",item.delete_metadata)
        dict.setdefault("disk_config",item.disk_config)
        dict.setdefault("existing",item.existing)
        dict.setdefault("find",item.find)
        dict.setdefault("flavor", item.flavor)#
        dict.setdefault("flavor_id", item.flavor_id)
        dict.setdefault("force_delete",item.force_delete)
        dict.setdefault("get",item.get)
        dict.setdefault("get_metadata",item.get_metadata)
        dict.setdefault("has_config_drive",item.has_config_drive)
        dict.setdefault("head",item.head)
        dict.setdefault("host_id", item.host_id)#
        dict.setdefault("id",item.id)#
        dict.setdefault("image", item.image)#
        dict.setdefault("image_id", item.image_id)#
        dict.setdefault("key_name", item.key_name)
        dict.setdefault("launched_at", item.launched_at)#
        dict.setdefault("links", item.links)#
        dict.setdefault("list",item.list)
        dict.setdefault("location",item.location)
        dict.setdefault("metadata", item.metadata)
        dict.setdefault("name", item.name)
        dict.setdefault("networks", item.networks)
        dict.setdefault("new",item.new)
        dict.setdefault("patch_update",item.patch_update)
        dict.setdefault("personality",item.personality)
        dict.setdefault("power_state",item.power_state)
        dict.setdefault("progress",item.progress)#
        dict.setdefault("project_id",item.project_id)#
        dict.setdefault("put_create",item.put_create)
        dict.setdefault("reboot",item.reboot)
        dict.setdefault("rebuild",item.rebuild)
        dict.setdefault("remove_security_group",item.remove_security_group)
        dict.setdefault("resize",item.resize)
        dict.setdefault("resource_key",item.resource_key)
        dict.setdefault("resources_key",item.resources_key)
        dict.setdefault("revert_resize",item.revert_resize)
        dict.setdefault("scheduler_hints",item.scheduler_hints)
        dict.setdefault("security_groups", item.security_groups)
        dict.setdefault("service",item.service)
        dict.setdefault("set_metadata",item.set_metadata)
        dict.setdefault("status", item.status)
        dict.setdefault("task_state",item.task_state)
        dict.setdefault("terminated_at",item.terminated_at)
        # dict.setdefault("to_dict",item.to_dict)#it seems this attr is used to extract data in a dict type
        dict.setdefault("update",item.update)
        dict.setdefault("updated_at",item.updated_at)#
        dict.setdefault("user_data",item.user_data)
        dict.setdefault("user_id",item.user_id)
        dict.setdefault("vm_state",item.vm_state)

        list.append(dict)
    print "output server data after extract"

    return list

#--------------result of dir(object):all function an attrs of the Server object-------------------
#['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__',
# '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_action', '_alternate_id', '_body', '_body_mapping', '_collect_attrs', '_consume_attrs',
# '_filter_component', '_get_id', '_get_mapping', '_get_one_match', '_header', '_header_mapping', '_metadata', '_prepare_request', '_query_mapping', '_translate_response', '_update',
# '_uri', '_uri_mapping', 'access_ipv4', 'access_ipv6', 'add_security_group', 'addresses', 'admin_password', 'allow_create', 'allow_delete', 'allow_get', 'allow_head', 'allow_list',
# 'allow_update', 'attached_volumes', 'availability_zone', 'base_path', 'block_device_mapping', 'change_password', 'confirm_resize', 'create', 'create_image', 'created_at', 'delete',
# 'delete_metadata', 'disk_config', 'existing', 'find', 'flavor', 'flavor_id', 'force_delete', 'get', 'get_metadata', 'has_config_drive', 'head', 'host_id', 'id', 'image', 'image_id',
# 'key_name', 'launched_at', 'links', 'list', 'location', 'metadata', 'name', 'networks', 'new', 'patch_update', 'personality', 'power_state', 'progress', 'project_id', 'put_create',
# 'reboot', 'rebuild', 'remove_security_group', 'resize', 'resource_key', 'resources_key', 'revert_resize', 'scheduler_hints', 'security_groups', 'service', 'set_metadata', 'status',
# 'task_state', 'terminated_at', 'to_dict', 'update', 'updated_at', 'user_data', 'user_id', 'vm_state']


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~List resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#A server is a virtual machine that provides access to a compute instance being run by your cloud provider.
def list_servers(conn):
    print("List OpenStack Servers:")
    servers = conn.compute.servers()
    for server in servers:
        print(server)
    list = extract_server(conn.compute.servers())
    return list

#****The output result is*******
    #openstack.compute.v2.server.Server(OS-EXT-STS:task_state=None,
#                                       addresses={u'private_alice': [{u'OS-EXT-IPS-MAC:mac_addr': u'fa:16:3e:66:85:a3',
#                                                                      u'version': 4,
#                                                                      u'addr': u'172.16.2.9',
#                                                                      u'OS-EXT-IPS:type': u'fixed'}]},
#                                       links=[{u'href': u'http://controller:8774/v2.1/7ad82b22a6924a978c54862efb3517f2/servers/1adafcac-d19c-4d84-bb19-ae296d298c63', u'rel': u'self'},
#                                              {u'href': u'http://controller:8774/7ad82b22a6924a978c54862efb3517f2/servers/1adafcac-d19c-4d84-bb19-ae296d298c63', u'rel': u'bookmark'}],
#                                       image={u'id': u'70122065-a0ed-4975-8ba3-1740cdaf3722',
#                                              u'links': [{u'href': u'http://controller:8774/7ad82b22a6924a978c54862efb3517f2/images/70122065-a0ed-4975-8ba3-1740cdaf3722',u'rel': u'bookmark'}]},
#                                       OS-EXT-STS:vm_state=active,
#                                       OS-SRV-USG:launched_at=2016-12-26T10:39:11.000000,
#                                       flavor={u'id': u'1',
#                                               u'links': [{u'href': u'http://controller:8774/7ad82b22a6924a978c54862efb3517f2/flavors/1', u'rel': u'bookmark'}]},
#                                       networks=[{'uuid': u'336e9e6e-4a1a-4a80-95ce-197e989e71a8'}],
#                                       security_groups=[{u'name': u'default'}],
#                                       user_id=8903fd567f124fc2911079499a8d0c50,
#                                       imageRef=70122065-a0ed-4975-8ba3-1740cdaf3722,
#                                       OS-DCF:diskConfig=MANUAL,
#                                       id=1adafcac-d19c-4d84-bb19-ae296d298c63,
#                                       accessIPv4=,
#                                       accessIPv6=,
#                                       progress=0,
#                                       OS-EXT-STS:power_state=1,
#                                       OS-EXT-AZ:availability_zone=nova,
#                                       config_drive=,
#                                       status=ACTIVE,
#                                       updated=2016-12-26T10:39:11Z,
#                                       hostId=bbf62531793666b4be82a43aaa477a40776f8dd70a8fc7301430cfc6,
#                                       OS-SRV-USG:terminated_at=None,
#                                       key_name=mykey,
#                                       flavorRef=1,
#                                       name=demo-alice-cirros1,
#                                       adminPass=iCvX5kDMKV8b,
#                                       tenant_id=7ad82b22a6924a978c54862efb3517f2,
#                                       created=2016-12-26T10:39:03Z,
#                                       os-extended-volumes:volumes_attached=[],
#                                       metadata={},
#                                       Location=http://controller:8774/v2.1/7ad82b22a6924a978c54862efb3517f2/servers/1adafcac-d19c-4d84-bb19-ae296d298c63)

#Before you create a VM, you should prepare below parameters:
#image,flavor,network,keypair


#An image is the operating system you want to use for your server.
def list_images(conn):
    print("List Images:")

    for image in conn.compute.images():
        print(image)
    return conn.compute.images()

#A flavor is the resource configuration for a server. Each flavor is a unique combination of disk, memory, vCPUs, and network bandwidth.
def list_flavors(conn):
    print("List Flavors:")

    for flavor in conn.compute.flavors():
        print(flavor)
    return conn.compute.flavors()

#A network provides connectivity to servers.
def list_networks(conn):
    print("List Networks:")

    for network in conn.network.networks():
        print(network)

    return conn.network.networks()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Find resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def find_image(conn,image_name):
    image = conn.compute.find_image(image_name)
    print 'The image we find is:'
    print image
    # ********result output
    # AttributeError: 'str' object has no attribute 'get'
    #
    # The image we find is:
    # openstack.compute.v2.image.Image(id=70122065-a0ed-4975-8ba3-1740cdaf3722,
    #                                  links=[{u'href': u'http://controller:8774/v2.1/2f1bc8c34f094d049a201819732537a3/images/70122065-a0ed-4975-8ba3-1740cdaf3722', u'rel': u'self'},
    #                                         {u'href': u'http://controller:8774/2f1bc8c34f094d049a201819732537a3/images/70122065-a0ed-4975-8ba3-1740cdaf3722', u'rel': u'bookmark'},
    #                                         {u'href': u'http://controller:9292/images/70122065-a0ed-4975-8ba3-1740cdaf3722', u'type': u'application/vnd.openstack.image', u'rel': u'alternate'}],
    #                                   name=cirros)
    # [26/Dec/2016 09:40:20] "GET /image_find/ HTTP/1.1" 500 59259
    #
    return image

def find_flavor(conn,flavor_name):
    flavor = conn.compute.find_flavor(flavor_name)
    print 'The flavor we find is'
    print flavor
    return flavor



def find_keypair(conn,keypair_name):
    keypair = conn.compute.find_keypair(keypair_name)
    print 'The keypair we find is'+ keypair
    return keypair




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delete resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def delete_key_pair(conn):
    pass


def delete_server(conn):
    conn.compute.delete_server()# The para value can be either the ID of a server or a Server instance.
    pass



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def create_keypair(conn,keypair_name,ssh_dir,private_keypair_file):
    keypair = conn.compute.find_keypair(keypair_name)

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name=keypair_name)
        print(keypair)

        try:
            os.mkdir(ssh_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open(private_keypair_file, 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod(private_keypair_file, 0o400)

    return keypair



def create_server(conn,server_name,image_name,flavor_name,network_name,private_keypair_file):
    print("Create Server:")

    image = conn.compute.find_image(image_name)
    flavor = conn.compute.find_flavor(flavor_name)
    network = conn.network.find_network(network_name)
    keypair = create_keypair(conn)

    server = conn.compute.create_server(
        name=server_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

    server = conn.compute.wait_for_server(server)

    print("ssh -i {key} root@{ip}".format(
        key=private_keypair_file,
        ip=server.access_ipv4))

    return server.access_ipv4



def create_server2(conn,server_name,image_name,flavor_name,network_name,private_keypair_name):
    print("Create Server:")

    image = conn.compute.find_image(image_name)
    print image.id
    flavor = conn.compute.find_flavor(flavor_name)
    print flavor.id
    network = conn.network.find_network(network_name)
    print network.id
    keypair = conn.compute.find_keypair(private_keypair_name)
    print keypair.id
    server = conn.compute.create_server(
        name=server_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

    server = conn.compute.wait_for_server(server)

    # print("ssh -i {key} root@{ip}".format(
    #     key=private_keypair_file,
    #     ip=server.access_ipv4))

    print server

    return server.access_ipv4



def create_server3(conn,server_name,image_id,flavor_name,network_id,private_keypair_name):
    print("Create Server:")

    image = conn.compute.find_image(image_id)
    print image.id
    flavor = conn.compute.find_flavor(flavor_name)
    print flavor.id
    network = conn.network.find_network(network_id)
    print network.id
    keypair = conn.compute.find_keypair(private_keypair_name)
    print keypair.id
    server = conn.compute.create_server(
        name=server_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

    server = conn.compute.wait_for_server(server)

    # print("ssh -i {key} root@{ip}".format(
    #     key=private_keypair_file,
    #     ip=server.access_ipv4))

    print server
    return server




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Modify resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def resize_server(conn,server,flavor):
    conn.compute.resize_server(server,flavor)
    pass




def create_server_image(conn,server,image_name,metadata=None):
    conn.compute.create_server_image(server, image_name, metadata=None)
    pass


def start_server(conn,server):
    conn.compute.start_server(server)
    pass


def stop_server(conn,server):
    conn.compute.stop_server(server)
    pass