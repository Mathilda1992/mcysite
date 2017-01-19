# mcy update in 2016-12-07
#Refer to :http://developer.openstack.org/sdks/python/openstacksdk/users/proxies/network.html

# List Networks
# List Subnets
# List Ports
# List Security Groups
# List Routers
# List Network Agents
# Create Network
# Delete Network
#......

from Iserlab.models import Network
from extract_openstack_data import *


def find_network(conn,network_id):
    network = conn.network.find_network(network_id)
    print 'The network we find is'+ network
    return network




# We use Networking Option 2: Self-service networks
# A network is an isolated Layer 2 networking segment.
# There are two types of networks, project and provider networks(external network).
# Project networks are fully isolated and are not shared with other projects.
# Provider networks map to existing physical networks in the data center and provide external network access for servers.
# Only an OpenStack administrator can create provider networks. Networks can be connected via routers.
def list_networks(conn):
    print("List Networks:")
    networks = conn.network.networks()
    for network in networks:
        print(network)
    return networks
    # output result*******
    # openstack.network.v2.network.Network(attrs={u'status': u'ACTIVE',
    #                                             u'subnets': [u'ce500f45-b8f9-42fa-a9e5-cd31b04b4822'],
    #                                             u'name': u'public',
    #                                             u'provider:physical_network': u'public',
    #                                             u'admin_state_up': True,
    #                                             u'tenant_id': u'2f1bc8c34f094d049a201819732537a3',
    #                                             u'mtu': 0,
    #                                             u'router:external': True,
    #                                             u'port_security_enabled': True,
    #                                             u'shared': True,
    #                                             u'provider:network_type': u'flat',
    #                                             u'id': u'4e9b7eea-fcd3-4773-bcb4-711b44979b18',
    #                                             u'provider:segmentation_id': None},
    #                                       loaded=True)



def convert_network(networks):
    networkDictList = extractnetwork(networks)
    print networkDictList
    for i in range(0,len(networkDictList)):
        print networkDictList[i]["attrs"]["subnets"]
    return networkDictList




# A subnet is a block of IP addresses and associated configuration state.
# Subnets are used to allocate IP addresses when new ports are created on a network.
def list_subnets(conn):
    print("List Subnets:")
    subnets = conn.network.subnets()
    for s in subnets:
         print s
    return subnets

def convert_subnet(subnets):
    # convert the openstack data into dict
    subnetsDictList = extractnetwork(subnets)
    print subnetsDictList
    for i in range(0, len(subnetsDictList)):
        print u'start:%s,end:%s,cidr:%s' % (subnetsDictList[i]["attrs"]["start"], subnetsDictList[i]["attrs"]["end"], subnetsDictList[i]["attrs"]["cidr"])
    return subnetsDictList




# A port is a connection point for attaching a single device, such as the NIC of a server, to a network.
# The port also describes the associated network configuration, such as the MAC and IP addresses to be used on that port.
def list_ports(conn):
    print("List Ports:")

    for port in conn.network.ports():
        print(port)


# A security group acts as a virtual firewall for servers.
# It is a container for security group rules which specify the type of network traffic and direction that is allowed to pass through a port.
# To create security_group,please go to compute_resource_operation.py
def list_security_groups(conn):
    print("List Security Groups:")

    for port in conn.network.security_groups():
        print(port)


# A router is a logical component that forwards data packets between networks.
# It also provides Layer 3 and NAT forwarding to provide external network access for servers on project networks.
def list_routers(conn):
    print("List Routers:")

    for router in conn.network.routers():
        print(router)


# A network agent is a plugin that handles various tasks used to implement virtual networks.
# These agents include neutron-dhcp-agent, neutron-l3-agent,
# neutron-metering-agent, and neutron-lbaas-agent, among others.
def list_network_agents(conn):
    print("List Network Agents:")

    for agent in conn.network.agents():
        print(agent)


# Create a project network and subnet. This network can be used when creating a server and
# allows the server to communicate with others servers on the same project network.

# I plan to give this function the required parameters of subnet createation by a python object
def create_network(conn, network_name, subnet_name, ip_version, cidr, gateway_ip,description,creator,is_shared):
    print("Create Network:")
    n1 = Network(
        network_name = network_name,
        network_description = description,
        owner = creator,
        is_shared = is_shared,
        subnet_name = subnet_name,
        ip_version=ip_version,
        cidr=cidr,
        gateway_ip=gateway_ip,
    )
    n1.save()


    new_network = conn.network.create_network(name=network_name)
    print(new_network)
    # openstack.network.v2.network.Network(attrs={u'status': u'ACTIVE',
                                                # u'subnets': [],
                                                # 'name': u'openstacksdk-example-project-network',
                                                # u'provider:physical_network': None,
                                                # u'admin_state_up': True,
                                                # u'tenant_id': u'2f1bc8c34f094d049a201819732537a3',
                                                # u'mtu': 0, 'headers': {'Date': 'Fri, 30 Dec 2016 05:42:26 GMT',
                                                #                        'Content-Length': '400',
                                                #                        'Connection': 'keep-alive',
                                                #                        'Content-Type': 'application/json; charset=UTF-8',
                                                #                        'X-Openstack-Request-Id': 'req-6d0094e2-67ca-4ae7-a513-b4c66c4bae23'},
                                                # u'router:external': False,
                                                # u'shared': False,
                                                # u'port_security_enabled': True,
                                                # u'provider:network_type': u'vxlan',
                                                # u'id': u'b0264201-213a-4bf0-a8cc-38ecfc404f47',
                                                # u'provider:segmentation_id': 35},
                                        # loaded=False)
    print new_network.id
    new_subnet = conn.network.create_subnet(
        name=subnet_name,
        network_id=new_network.id,
        ip_version=ip_version,
        cidr=cidr,
        gateway_ip=gateway_ip)
    print(new_subnet)
    #openstack.network.v2.subnet.Subnet(attrs={u'ipv6_ra_mode': None,
                                             # u'allocation_pools': [{u'start': u'10.0.2.2', u'end': u'10.0.2.254'}],
                                             # u'host_routes': [],
                                             # u'ipv6_address_mode': None,
                                             # 'cidr': u'10.0.2.0/24',
                                             # u'id': u'9522ec40-a350-478a-8eb3-ffeeb4df34b9',
                                             # u'subnetpool_id': None,
                                             # 'name': u'openstacksdk-example-project-subnet',
                                             # u'enable_dhcp': True,
                                             # 'network_id': u'b0264201-213a-4bf0-a8cc-38ecfc404f47',
                                             # u'tenant_id': u'2f1bc8c34f094d049a201819732537a3',
                                             # u'dns_nameservers': [],
                                             # 'headers': {'Date': 'Fri, 30 Dec 2016 06:01:38 GMT', 'Content-Length': '475', 'Connection': 'keep-alive', 'Content-Type': 'application/json; charset=UTF-8', 'X-Openstack-Request-Id': 'req-7e320362-148b-4893-be08-6e03d53113ce'},
                                             # 'gateway_ip': u'10.0.2.1',
                                             # 'ip_version': 4},
                                    # loaded=False)

    #analyse the network object data into a dict!!!!!!!

    #update the record in db


    return n1.cidr




# Delete a project network and its subnets.
# Before delete the subnet, we should make sure all related interfaces should not exist
def delete_network(conn,n_id):
    print("Delete Network:")

    example_network = conn.network.find_network(
        'openstacksdk-example-project-network')

    for example_subnet in example_network.subnet_ids:
        conn.network.delete_subnet(example_subnet, ignore_missing=False)
    conn.network.delete_network(example_network, ignore_missing=False)


    #delete from Network DB
    Network.objects.filter(id=n_id).delete()

    return 0



#/*****************************************************************/
#update_network(network, **attrs)
#Update a network
# Parameters:
#   network - Either the id of a network or an instance of type:Network
#   attrs (dict) - The attributes to update on the network represented by network
#Returns:
#   The updated network
# Return type
#   Network

#/*****************************************************************/
def update_network(conn,network,n_dict):
    print ' Update the network'
    new_n = conn.network.update_network(network,n_dict)
    pass



def create_router(conn,router_dict):
    new_router = conn.network.create_router(router_dict)
    pass



#/*****************************************************************/
#add_gateway_to_router(router, **body)
# Add Gateway to a router
#
# Parameters:
# router - Either the router ID or an instance of Router
# body - Body with the gateway information
# Returns:
# Router with updated interface
#
# Return type:
# class:	~openstack.network.v2.router.Router
#/*****************************************************************/
def add_gateway_to_router(conn,router,public_net_name):
    print 'Add the router to public net'
    router = conn.network.add_gateway_to_router(router,public_net_name)
    pass


def remove_gateway_to_router(conn,router,public_net_name):
    print 'Remove the router to public net'
    router = conn.network.remove_gateway_to_router(router,public_net_name)
    pass


def add_interface_to_router(conn,router,subnet_id,port_id=None):
    print 'Add the subnet to router'
    router = conn.network.add_interface_to_router(router,subnet_id=None,port_id=None)
    return router


def remove_interface_to_router(conn,router,subnet_id,port_id=None):
    print 'Remove the subnet to router'
    router = conn.network.remove_interface_to_router(router,subnet_id=None,port_id=None)
    return router