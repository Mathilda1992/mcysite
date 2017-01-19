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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~List resource~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#A server is a virtual machine that provides access to a compute instance being run by your cloud provider.
def list_servers(conn):
    print("List Servers:")

    for server in conn.compute.servers():
        print(server)
    return conn.compute.servers()

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
#                                       imageRef=70122065-a0ed-4975-8ba3-1740cdaf3722, OS-DCF:diskConfig=MANUAL,
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