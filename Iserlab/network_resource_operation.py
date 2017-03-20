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



def extract_router(router):
    dict = {}
    dict.setdefault("add_gateway", router.add_gateway)#
    dict.setdefault("add_interface",router.add_interface)#
    dict.setdefault("admin_state_up",router.admin_state_up)
    dict.setdefault("allow_create",router.allow_create)
    dict.setdefault("allow_delete",router.allow_delete)#
    dict.setdefault("allow_head",router.allow_head)
    dict.setdefault("allow_list",router.allow_list)
    dict.setdefault("allow_retrieve",router.allow_retrieve)
    dict.setdefault("allow_update",router.allow_update)
    dict.setdefault("availability_zone_hints",router.availability_zone_hints)
    dict.setdefault("availability_zones",router.availability_zones)
    dict.setdefault("base_path",router.base_path)
    dict.setdefault("clear",router.clear)
    dict.setdefault("convert_ids",router.convert_ids)
    dict.setdefault("create",router.create)
    dict.setdefault("create_by_id",router.create_by_id)
    dict.setdefault("created_at",router.created_at)#
    dict.setdefault("delete",router.delete)
    dict.setdefault("from_name",router.from_name)
    dict.setdefault("get",router.get)
    dict.setdefault("get_by_id",router.get_by_id)
    dict.setdefault("get_data_by_id",router.get_data_by_id)
    dict.setdefault("get_headers",router.get_headers)
    dict.setdefault("get_id",router.get_id)
    dict.setdefault("get_resource_name",router.get_resource_name)
    dict.setdefault("ha",router.ha)
    dict.setdefault("head",router.head)
    dict.setdefault("head_by_id",router.head_by_id)
    dict.setdefault("head_data_by_id",router.head_data_by_id)
    dict.setdefault("id",router.id)#
    dict.setdefault("id_attribute",router.id_attribute)
    dict.setdefault("is_admin_state_up",router.is_admin_state_up)
    dict.setdefault("is_dirty",router.is_dirty)
    dict.setdefault("is_distributed",router.is_distributed)
    dict.setdefault("is_ha",router.is_ha)
    # dict.setdefault("items",router.items)
    # dict.setdefault("iteritems",router.iteritems)
    # dict.setdefault("iterkeys",router.iterkeys)
    # dict.setdefault("itervalues",router.itervalues)
    dict.setdefault("keys",router.keys)
    dict.setdefault("list",router.list)
    dict.setdefault("location",router.location)
    dict.setdefault("remove_interface",router.remove_interface)
    dict.setdefault("resource_key",router.resource_key)
    dict.setdefault("resource_name",router.resource_name)
    dict.setdefault("resources_key",router.resources_key)
    dict.setdefault("revision_number",router.revision_number)
    dict.setdefault("routes",router.routes)
    dict.setdefault("service",router.service)
    dict.setdefault("set_headers",router.set_headers)
    dict.setdefault("setdefault",router.setdefault )
    dict.setdefault("status",router.status )#
    dict.setdefault("tenant_id",router.tenant_id )
    # dict.setdefault("to_dict",router.to_dict )
    dict.setdefault("update",router.update )
    dict.setdefault("update_attrs",router.update_attrs )
    dict.setdefault("update_by_id",router.update_by_id )
    dict.setdefault("updated_at",router.updated_at )#
    # dict.setdefault("values",router.values )

    return dict

#['_MutableMapping__marker', '__abstractmethods__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__doc__', '__eq__',
# '__format__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__metaclass__', '__module__', '__ne__', '__new__',
# '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abc_cache',
#  '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry', '_attrs', '_dirty', '_from_attr', '_get_create_body', '_get_url', '_loaded',
#  '_reset_dirty', '_update_attrs_from_response', 'add_gateway', 'add_interface', 'admin_state_up', 'allow_create', 'allow_delete', 'allow_head',
# 'allow_list', 'allow_retrieve', 'allow_update', 'availability_zone_hints', 'availability_zones', 'base_path', 'clear', 'convert_ids', 'create',
# 'create_by_id', 'created_at', 'delete', 'delete_by_id', 'description', 'distributed', 'existing', 'external_gateway_info', 'find', 'from_id',
# 'from_name', 'get', 'get_by_id', 'get_data_by_id', 'get_headers', 'get_id', 'get_resource_name', 'ha', 'head', 'head_by_id', 'head_data_by_id',
# 'id', 'id_attribute', 'is_admin_state_up', 'is_dirty', 'is_distributed', 'is_ha', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'list',
# 'location', 'name', 'name_attribute', 'new', 'patch_update', 'pop', 'popitem', 'project_id', 'remove_gateway', 'remove_interface', 'resource_key',
# 'resource_name', 'resources_key', 'revision_number', 'routes', 'service', 'set_headers', 'setdefault', 'status', 'tenant_id', 'to_dict', 'update',
# 'update_attrs', 'update_by_id', 'updated_at', 'values']




def extract_port(port):

    dict ={}
    dict.setdefault("admin_state_up",port.admin_state_up )#
    dict.setdefault("allow_create",port.allow_create )
    dict.setdefault("allow_delete",port.allow_delete )
    dict.setdefault("allow_head",port.allow_head )
    dict.setdefault("allow_list",port.allow_list )
    dict.setdefault("allow_retrieve",port.allow_retrieve )
    dict.setdefault("allow_update",port.allow_update )
    dict.setdefault("allowed_address_pairs",port.allowed_address_pairs )
    dict.setdefault("base_path",port.base_path )
    # dict.setdefault("binding:host_id",port.binding:host_id )
    # dict.setdefault("binding:profile",port.binding:profile )
    # dict.setdefault("binding:vif_details",port.binding:vif_details )
    dict.setdefault("binding_vif_type",port.binding_vif_type )
    dict.setdefault("binding_vnic_type",port.binding_vnic_type )
    dict.setdefault("clear",port.clear )
    dict.setdefault("convert_ids",port.convert_ids )
    dict.setdefault("create",port.create)
    dict.setdefault("create_by_id",port.create_by_id )
    dict.setdefault("created_at",port.created_at )
    dict.setdefault("delete",port.delete )
    dict.setdefault("description",port.description )
    dict.setdefault("device_id",port.device_id )
    dict.setdefault("device_owner",port.device_owner )
    dict.setdefault("dns_assignment",port.dns_assignment )
    dict.setdefault("dns_name",port.dns_name )
    dict.setdefault("existing",port.existing )
    dict.setdefault("extra_dhcp_opts",port.extra_dhcp_opts )
    dict.setdefault("find",port.find )
    dict.setdefault("fixed_ips",port.fixed_ips )
    dict.setdefault("from_id",port.from_id )
    dict.setdefault("from_name",port.from_name )
    dict.setdefault("get",port.get )
    dict.setdefault("get_by_id",port.get_by_id )
    dict.setdefault("head_data_by_id",port.head_data_by_id )
    dict.setdefault("id",port.id )#
    dict.setdefault("id_attribute",port.id_attribute )
    dict.setdefault("is_admin_state_up",port.is_admin_state_up )
    dict.setdefault("is_dirty",port.is_dirty )
    dict.setdefault("is_port_security_enabled",port.is_port_security_enabled )
    # dict.setdefault("items",port.items )
    # dict.setdefault("iteritems",port.iteritems )
    # dict.setdefault("iterkeys",port.iterkeys )
    # dict.setdefault("itervalues",port.itervalues )
    dict.setdefault("keys",port.keys )
    dict.setdefault("list",port.list )
    dict.setdefault("location",port.location )
    dict.setdefault("mac_address",port.mac_address )
    dict.setdefault("name",port.name )#
    dict.setdefault("name_attribute",port.name_attribute )
    dict.setdefault("network_id",port.network_id )#
    dict.setdefault("new",port.new )
    dict.setdefault("patch_update",port.patch_update )
    dict.setdefault("pop",port.pop )
    dict.setdefault("popitem",port.popitem )
    dict.setdefault("port_security_enabled",port.port_security_enabled )
    dict.setdefault("project_id",port.project_id )#
    dict.setdefault("qos_policy_id",port.qos_policy_id )
    dict.setdefault("resource_key",port.resource_key )
    dict.setdefault("resource_name",port.resource_name )
    dict.setdefault("resources_key",port.resources_key )
    dict.setdefault("revision_number",port.revision_number )
    dict.setdefault("security_group_ids",port.security_group_ids )#
    # dict.setdefault("security_groups",port.security_groups )
    dict.setdefault("service",port.service )
    dict.setdefault("set_headers",port.set_headers )
    dict.setdefault("setdefault",port.setdefault )
    dict.setdefault("status",port.status )#
    dict.setdefault("tenant_id",port.tenant_id )#
    # dict.setdefault("to_dict",port.to_dict )
    dict.setdefault("update",port.update )
    dict.setdefault("update_attrs",port.update_attrs )
    dict.setdefault("update_by_id",port.update_by_id )
    dict.setdefault("updated_at",port.updated_at )
    # dict.setdefault("values",port.values )


    return dict


def extract_topo(topo):
    pass



def extract_network(networks,subnets):
    list = []
    for i in range(0, networks.__len__()):
        # print networks[i]
        dict = {}
        dict.setdefault("admin_state_up",networks[i].admin_state_up)#
        dict.setdefault("allow_create", networks[i].allow_create)
        dict.setdefault("allow_delete", networks[i].allow_delete)
        dict.setdefault("allow_head", networks[i].allow_head)
        dict.setdefault("allow_list", networks[i].allow_list)
        dict.setdefault("allow_retrieve", networks[i].allow_retrieve)
        dict.setdefault("allow_update", networks[i].allow_update)
        dict.setdefault("availability_zone_hints", networks[i].availability_zone_hints)
        dict.setdefault("availability_zones", networks[i].availability_zones)
        dict.setdefault("base_path", networks[i].base_path)
        dict.setdefault("clear", networks[i].clear)
        dict.setdefault("convert_ids", networks[i].convert_ids)
        dict.setdefault("create", networks[i].create)
        dict.setdefault("create_by_id", networks[i].create_by_id)
        dict.setdefault("created_at", networks[i].created_at)
        dict.setdefault("delete", networks[i].delete)
        dict.setdefault("delete_by_id", networks[i].delete_by_id)
        dict.setdefault("description", networks[i].description)
        dict.setdefault("dns_domain", networks[i].dns_domain)
        # dict.setdefault("existing", networks[i].existing )
        dict.setdefault("find", networks[i].find)
        dict.setdefault("from_id", networks[i].from_id)
        dict.setdefault("from_name", networks[i].from_name )
        dict.setdefault("get", networks[i].get)
        dict.setdefault("get_by_id", networks[i].get_by_id)
        dict.setdefault("get_data_by_id", networks[i].get_data_by_id )
        dict.setdefault("get_headers", networks[i].get_headers)
        dict.setdefault("get_id", networks[i].get_id)
        dict.setdefault("get_resource_name", networks[i].get_resource_name)
        dict.setdefault("head", networks[i].head)
        dict.setdefault("head_by_id", networks[i].head_by_id)
        dict.setdefault("head_data_by_id", networks[i].head_data_by_id )
        dict.setdefault("id", networks[i].id)#
        dict.setdefault("id_attribute", networks[i].id_attribute)
        dict.setdefault("ipv4_address_scope_id", networks[i].ipv4_address_scope_id)
        dict.setdefault("ipv6_address_scope_id", networks[i].ipv6_address_scope_id )
        dict.setdefault("is_admin_state_up", networks[i].is_admin_state_up)
        dict.setdefault("is_default", networks[i].is_default)
        dict.setdefault("is_dirty", networks[i].is_dirty )
        dict.setdefault("is_port_security_enabled", networks[i].is_port_security_enabled)
        dict.setdefault("is_router_external", networks[i].is_router_external)
        dict.setdefault("is_shared", networks[i].is_shared )
        dict.setdefault("items", networks[i].items)
        # dict.setdefault("iteritems", networks[i].iteritems )
        # dict.setdefault("iterkeys", networks[i].iterkeys)
        # dict.setdefault("itervalues", networks[i].itervalues)
        dict.setdefault("keys", networks[i].keys )
        dict.setdefault("list", networks[i].list)
        dict.setdefault("location", networks[i].location)
        dict.setdefault("mtu", networks[i].mtu)#
        dict.setdefault("name", networks[i].name)#
        dict.setdefault("name_attribute", networks[i].name_attribute )
        dict.setdefault("new", networks[i].new)
        dict.setdefault("patch_update", networks[i].patch_update)
        dict.setdefault("pop", networks[i].pop )
        dict.setdefault("popitem", networks[i].popitem)
        dict.setdefault("port_security_enabled", networks[i].port_security_enabled)
        dict.setdefault("project_id", networks[i].project_id)#
        # dict.setdefault("provider:physical_network", networks[i].physical_network)
        # dict.setdefault("provider:network_type",networks[i].network_type)
        # dict.setdefault("provider:segmentation_id",networks[i].provider)
        dict.setdefault("provider_network_type", networks[i].provider_network_type )#
        dict.setdefault("provider_physical_network", networks[i].provider_physical_network)#
        dict.setdefault("provider_segmentation_id", networks[i].provider_segmentation_id)#
        dict.setdefault("resource_key", networks[i].resource_key )
        dict.setdefault("resource_name", networks[i].resource_name)
        dict.setdefault("resources_key", networks[i].resources_key)
        dict.setdefault("revision_number", networks[i].revision_number )
        # dict.setdefault("router:external", networks[i].router:external)
        dict.setdefault("segments", networks[i].segments)
        dict.setdefault("service", networks[i].service)
        dict.setdefault("set_headers", networks[i].set_headers )
        dict.setdefault("setdefault", networks[i].setdefault)
        dict.setdefault("shared", networks[i].shared)
        dict.setdefault("status", networks[i].status)
        dict.setdefault("subnet_ids", networks[i].subnet_ids)
        dict.setdefault("subnets", networks[i].subnets)#
        dict.setdefault("tenant_id", networks[i].tenant_id)
        # dict.setdefault("to_dict", networks[i].to_dict )
        dict.setdefault("update", networks[i].update)
        dict.setdefault("update_attrs", networks[i].update_attrs)
        dict.setdefault("update_by_id", networks[i].update_by_id )
        dict.setdefault("updated_at", networks[i].updated_at)#
        # dict.setdefault("values", networks[i].values)

        for j in range(0, subnets.__len__()):
            if (networks[i].subnets[0] == subnets[j].id):
                dict.setdefault("sub_allocation_pools", subnets[j].allocation_pools)#
                dict.setdefault("sub_allow_create", subnets[j].allow_create )
                dict.setdefault("sub_allow_delete", subnets[j].allow_delete)
                dict.setdefault("sub_allow_head", subnets[j].allow_head)
                dict.setdefault("sub_allow_list", subnets[j].allow_list)
                dict.setdefault("sub_allow_retrieve", subnets[j].allow_retrieve)
                dict.setdefault("sub_allow_update", subnets[j].allow_update)
                dict.setdefault("sub_base_path", subnets[j].base_path)
                dict.setdefault("sub_cidr", subnets[j].cidr)#
                dict.setdefault("sub_clear", subnets[j].clear)
                dict.setdefault("sub_convert_ids", subnets[j].convert_ids)
                dict.setdefault("sub_create", subnets[j].create)
                dict.setdefault("sub_create_by_id", subnets[j].create_by_id)
                dict.setdefault("sub_created_at", subnets[j].created_at)#
                dict.setdefault("sub_delete", subnets[j].delete)
                dict.setdefault("sub_delete_by_id", subnets[j].delete_by_id)
                dict.setdefault("sub_description", subnets[j].description)
                dict.setdefault("sub_dns_nameservers", subnets[j].dns_nameservers)#
                dict.setdefault("sub_enable_dhcp", subnets[j].enable_dhcp)#
                dict.setdefault("sub_existing", subnets[j].existing)
                dict.setdefault("sub_find", subnets[j].find)
                dict.setdefault("sub_from_id", subnets[j].from_id)
                dict.setdefault("sub_from_name", subnets[j].from_name)
                dict.setdefault("sub_gateway_ip", subnets[j].gateway_ip)#
                dict.setdefault("sub_get", subnets[j].get)
                dict.setdefault("sub_get_by_id", subnets[j].get_by_id)
                dict.setdefault("sub_get_data_by_id", subnets[j].get_data_by_id)
                dict.setdefault("sub_get_headers", subnets[j].get_headers)
                dict.setdefault("sub_get_id", subnets[j].get_id)
                dict.setdefault("sub_get_resource_name", subnets[j].get_resource_name)
                dict.setdefault("sub_head", subnets[j].head)
                dict.setdefault("sub_head_by_id", subnets[j].head_by_id)
                dict.setdefault("sub_head_data_by_id", subnets[j].head_data_by_id)
                dict.setdefault("sub_host_routes", subnets[j].host_routes)#
                dict.setdefault("sub_id", subnets[j].id)#
                dict.setdefault("sub_id_attribute", subnets[j].id_attribute)
                dict.setdefault("sub_ip_version", subnets[j].ip_version)#
                dict.setdefault("sub_ipv6_address_mode", subnets[j].ipv6_address_mode)#
                dict.setdefault("sub_ipv6_ra_mode", subnets[j].ipv6_ra_mode)#
                dict.setdefault("sub_is_dhcp_enabled", subnets[j].is_dhcp_enabled)#
                dict.setdefault("sub_is_dirty", subnets[j].is_dirty)
                dict.setdefault("sub_items", subnets[j].items)
                # dict.setdefault("sub_iteritems", subnets[j].iteritems)
                # dict.setdefault("sub_iterkeys", subnets[j].iterkeys)
                # dict.setdefault("sub_itervalues", subnets[j].itervalues)
                dict.setdefault("sub_keys", subnets[j].keys)
                dict.setdefault("sub_list", subnets[j].list)
                dict.setdefault("sub_location", subnets[j].location)
                dict.setdefault("sub_name", subnets[j].name)
                dict.setdefault("sub_name_attribute", subnets[j].name_attribute)
                dict.setdefault("sub_network_id", subnets[j].network_id)
                dict.setdefault("sub_new", subnets[j].new)
                dict.setdefault("sub_patch_update", subnets[j].patch_update)
                dict.setdefault("sub_pop", subnets[j].pop)
                # dict.setdefault("sub_popitem", subnets[j].popitem)
                dict.setdefault("sub_project_id", subnets[j].project_id)
                dict.setdefault("sub_resource_key", subnets[j].resource_key)
                dict.setdefault("sub_resource_name", subnets[j].resource_name)
                dict.setdefault("sub_resources_key", subnets[j].resources_key)
                dict.setdefault("sub_revision_number", subnets[j].revision_number)
                dict.setdefault("sub_segment_id", subnets[j].segment_id)
                dict.setdefault("sub_service", subnets[j].service)
                dict.setdefault("sub_service_types", subnets[j].service_types)
                dict.setdefault("sub_set_headers", subnets[j].set_headers)
                dict.setdefault("sub_setdefault", subnets[j].setdefault)
                dict.setdefault("subnetpool_id", subnets[j].subnetpool_id)#
                dict.setdefault("sub_subnet_pool_id", subnets[j].subnet_pool_id)
                dict.setdefault("sub_tenant_id", subnets[j].tenant_id)#
                # dict.setdefault("sub_to_dict", subnets[j].to_dict)
                dict.setdefault("sub_update", subnets[j].update)
                dict.setdefault("sub_update_attrs", subnets[j].update_attrs)
                dict.setdefault("sub_update_by_id", subnets[j].update_by_id)
                dict.setdefault("sub_updated_at", subnets[j].updated_at)
                # dict.setdefault("sub_values", subnets[j].values)

        list.append(dict)
    return list

    #-----------result of dir(network): all attrs of Network object-----------------------------
    #['_MutableMapping__marker', '__abstractmethods__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__',
    # '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__metaclass__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
    # '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abc_cache', '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry', '_attrs', '_dirty',
    # '_from_attr', '_get_create_body', '_get_url', '_loaded', '_reset_dirty', '_update_attrs_from_response', 'admin_state_up', 'allow_create', 'allow_delete', 'allow_head', 'allow_list',
    # 'allow_retrieve', 'allow_update', 'availability_zone_hints', 'availability_zones', 'base_path', 'clear', 'convert_ids', 'create', 'create_by_id', 'created_at', 'delete', 'delete_by_id',
    # 'description', 'dns_domain', 'existing', 'find', 'from_id', 'from_name', 'get', 'get_by_id', 'get_data_by_id', 'get_headers', 'get_id', 'get_resource_name', 'head', 'head_by_id',
    # 'head_data_by_id', 'id', 'id_attribute', 'ipv4_address_scope_id', 'ipv6_address_scope_id', 'is_admin_state_up', 'is_default', 'is_dirty', 'is_port_security_enabled', 'is_router_external',
    # 'is_shared', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'list', 'location', 'mtu', 'name', 'name_attribute', 'new', 'patch_update', 'pop', 'popitem', 'port_security_enabled',
    # 'project_id', 'provider:network_type', 'provider:physical_network', 'provider:segmentation_id', 'provider_network_type', 'provider_physical_network', 'provider_segmentation_id',
    # 'resource_key', 'resource_name', 'resources_key', 'revision_number', 'router:external', 'segments', 'service', 'set_headers', 'setdefault', 'shared', 'status', 'subnet_ids', 'subnets',
    # 'tenant_id', 'to_dict', 'update', 'update_attrs', 'update_by_id', 'updated_at', 'values']


    # -----------result of dir(subnet): all attrs of Subnet object-----------------------------
    #['_MutableMapping__marker', '__abstractmethods__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__',
    # '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__metaclass__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
    # '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abc_cache', '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry', '_attrs', '_dirty',
    # '_from_attr', '_get_create_body', '_get_url', '_loaded', '_reset_dirty', '_update_attrs_from_response', 'allocation_pools', 'allow_create', 'allow_delete', 'allow_head', 'allow_list',
    # 'allow_retrieve', 'allow_update', 'base_path', 'cidr', 'clear', 'convert_ids', 'create', 'create_by_id', 'created_at', 'delete', 'delete_by_id', 'description', 'dns_nameservers',
    # 'enable_dhcp', 'existing', 'find', 'from_id', 'from_name', 'gateway_ip', 'get', 'get_by_id', 'get_data_by_id', 'get_headers', 'get_id', 'get_resource_name', 'head', 'head_by_id',
    # 'head_data_by_id', 'host_routes', 'id', 'id_attribute', 'ip_version', 'ipv6_address_mode', 'ipv6_ra_mode', 'is_dhcp_enabled', 'is_dirty', 'items', 'iteritems', 'iterkeys', 'itervalues',
    # 'keys', 'list', 'location', 'name', 'name_attribute', 'network_id', 'new', 'patch_update', 'pop', 'popitem', 'project_id', 'resource_key', 'resource_name', 'resources_key', 'revision_number',
    # 'segment_id', 'service', 'service_types', 'set_headers', 'setdefault', 'subnet_pool_id', 'subnetpool_id', 'tenant_id', 'to_dict', 'update', 'update_attrs', 'update_by_id', 'updated_at',
    # 'values']



def list_networks2(conn):
    networks =conn.network.networks()
    subnets = conn.network.subnets()
    NetworkList =[]
    SubnetList =[]
    for i in networks:
        NetworkList.append(i)
    for i in subnets:
        SubnetList.append(i)
    print NetworkList[0]
    list = extract_network(NetworkList,SubnetList)
    print "List network after extract"

    return list



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
        # print dir(network)
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

    #openstack.network.v2.network.Network(attrs={u'status': u'ACTIVE',
                                                # u'subnets': [u'e9a98c9a-67af-4727-a3ee-57c3b1098c49'],
                                                # u'name': u'mcy-network222',
                                                # u'provider:physical_network': None,
                                                # u'admin_state_up': True,
                                                # u'tenant_id': u'2f1bc8c34f094d049a201819732537a3',
                                                # u'mtu': 0,
                                                # u'router:external': False,
                                                # u'port_security_enabled': True,
                                                # u'shared': False,
                                                # u'provider:network_type': u'vxlan',
                                                # u'id': u'8b0791f1-90c3-4241-b899-fe6060f22241',
                                                # u'provider:segmentation_id': 9},
                                        # loaded=True)


    # openstack.network.v2.network.Network(attrs={u'status': u'ACTIVE',
                                                    # u'subnets': [],
                                                    # u'name': u'openstacksdk-example-project-network',
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


# def convert_network(networks):
#     networkDictList = extractnetwork(networks)
#     print networkDictList
#     for i in range(0,len(networkDictList)):
#         print networkDictList[i]["attrs"]["subnets"]
#     return networkDictList



# A subnet is a block of IP addresses and associated configuration state.
# Subnets are used to allocate IP addresses when new ports are created on a network.
def list_subnets(conn):
    print("List Subnets:")
    subnets = conn.network.subnets()
    return subnets
    #openstack.network.v2.subnet.Subnet(attrs={u'name': u'mcy-subnet222',
                                                # u'enable_dhcp': True,
                                                # u'network_id': u'8b0791f1-90c3-4241-b899-fe6060f22241',
                                                # u'tenant_id': u'2f1bc8c34f094d049a201819732537a3',
                                                # u'dns_nameservers': [],
                                                # u'ipv6_ra_mode': None,
                                                # u'allocation_pools': [{u'start': u'10.0.5.2', u'end': u'10.0.5.254'}],
                                                # u'host_routes': [],
                                                # u'ipv6_address_mode': None,
                                                # u'ip_version': 4,
                                                # u'gateway_ip': u'10.0.5.1',
                                                # u'cidr': u'10.0.5.0/24',
                                                # u'id': u'e9a98c9a-67af-4727-a3ee-57c3b1098c49',
                                                # u'subnetpool_id': None},
                                        # loaded=True)


    # openstack.network.v2.subnet.Subnet(attrs={u'ipv6_ra_mode': None,
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



# def convert_subnet(subnets):
#     # convert the openstack data into dict
#     subnetsDictList = extractnetwork(subnets)
#     print subnetsDictList
#     for i in range(0, len(subnetsDictList)):
#         print u'start:%s,end:%s,cidr:%s' % (subnetsDictList[i]["attrs"]["start"], subnetsDictList[i]["attrs"]["end"], subnetsDictList[i]["attrs"]["cidr"])
#     return subnetsDictList




# A port is a connection point for attaching a single device, such as the NIC of a server, to a network.
# The port also describes the associated network configuration, such as the MAC and IP addresses to be used on that port.
def list_ports(conn):
    ports =conn.network.ports()
    list =[]
    for port in ports:
        list.append(port.to_dict)
    return list
# openstack.network.v2.port.Port(attrs={u'status': u'ACTIVE',
                                        # u'binding:host_id': u'compute4',
                                        # u'allowed_address_pairs': [],
                                        # u'extra_dhcp_opts': [],
                                        # u'mac_address': u'fa:16:3e:8b:de:d4',
                                        # u'dns_assignment': [{u'hostname': u'host-172-16-1-25',
                                                            # u'ip_address': u'172.16.1.25',
                                                            # u'fqdn': u'host-172-16-1-25.openstacklocal.'}],
                                        # u'device_owner': u'compute:nova',
                                        # u'binding:profile': {},
                                        # u'port_security_enabled': True,
                                        # u'fixed_ips': [{u'subnet_id': u'e7d4b480-94d7-45dc-80e4-34c027b4cd33', u'ip_address': u'172.16.1.25'}],
                                        # u'id': u'73da2c08-98d7-4505-9432-133424949e22',
                                        # u'security_groups': [u'a9f050a3-6143-4da7-ac16-ff09ca397939'],
                                        # u'device_id': u'c90a1ba0-6cfb-47f5-920b-5197e12bdfea',
                                        # u'name': u'',
                                        # u'admin_state_up': True,
                                        # u'network_id': u'90684ef6-4c4b-4390-b08b-775f7086bf09',
                                        # u'dns_name': u'',
                                        # u'binding:vif_details': {u'port_filter': True},
                                        # u'binding:vnic_type': u'normal',
                                        # u'binding:vif_type': u'bridge',
                                        # u'tenant_id': u'02d5ad020bec441185dd901f61cb28db'},
                                # loaded=True)



def create_ports(conn,**attrs):
    new_port = conn.network.create_port(**attrs)
    return new_port.to_dict



def update_ports(conn,**attrs):
    update_port = conn.network.update_port(**attrs)
    return update_port.to_dict



def delete_port(conn,port_id):
    conn.network.delete_port(port_id,ignore_missing=False)



def get_port(conn,port_id):
    port = conn.network.get_port(port_id)
    print port.to_dict
    return port.to_dict



def find_port(conn,port_id):
    port = conn.network.find_port(port_id)
    return port.to_dict



# A security group acts as a virtual firewall for servers.
# It is a container for security group rules which specify the type of network traffic and direction that is allowed to pass through a port.
# To create security_group,please go to compute_resource_operation.py
def list_security_groups(conn):
    sgList =[]
    for sg in conn.network.security_groups():
        sgList.append(sg.to_dict)
    return sgList


def create_security_group(conn,**attrs):
    new_sg = conn.network.create_security_group(**attrs)
    return new_sg.to_dict


def delete_security_group(conn,sg_id):
    conn.network.delete_security_group(sg_id,ignore_missing=False)

def get_security_group(conn,sg_id):
    sg = conn.network.get_security_group(sg_id)
    return sg.to_dict

def list_security_group_rules(conn):
    sgr = conn.network.security_group_rules()
    list =[]
    for item in sgr:
        list.append(item.to_dict)
    return list

def create_security_group_rule(conn,**attrs):
    new = conn.network.create_security_group_rule(**attrs)
    return new.to_dict

def get_security_group_rule(conn,sgr_id):
    sgr = conn.network.get_security_group_rule(sgr_id)
    return sgr.to_dict

def delete_security_group_rule(conn,sgr_id):
    conn.network.delete_security_group_rule(sgr_id,ignore_missing=False)

# A network agent is a plugin that handles various tasks used to implement virtual networks.
# These agents include neutron-dhcp-agent, neutron-l3-agent,
# neutron-metering-agent, and neutron-lbaas-agent, among others.
def list_network_agents(conn):
    for agent in conn.network.agents():
        print(agent)



# Create a project network and subnet. This network can be used when creating a server and
# allows the server to communicate with others servers on the same project network.
# I plan to give this function the required parameters of subnet createation by a python object
def create_network(conn, network_name, subnet_name, ip_version, cidr, gateway_ip):
    print("Create Network:")
    new_network = conn.network.create_network(name=network_name)
    list1 =[]
    list1.append(new_network)
    # print(new_network)
    # print new_network.id
    new_subnet = conn.network.create_subnet(
        name=subnet_name,
        network_id=new_network.id,
        ip_version=ip_version,
        cidr=cidr,
        gateway_ip=gateway_ip)
    # print(new_subnet)
    list2=[]
    list2.append(new_subnet)

    #analyse the network object data into a dict!!!!!!!
    list=extract_network(list1,list2)
    return list



# Delete a project network and its subnets.
# Before delete the subnet, we should make sure all related interfaces should not exist
def delete_network(conn,n_id):
    print("Delete Network:")
    example_network = conn.network.find_network(n_id)
    #before delete net, should make sure all subnet belong to this net to be deleted
    for example_subnet in example_network.subnet_ids:
        conn.network.delete_subnet(example_subnet, ignore_missing=False)
    conn.network.delete_network(example_network, ignore_missing=False)



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
def update_network(conn,network_id,n_dict,subnet_id,sn_dict):
    print ' Update the network'
    update_net = conn.network.update_network(network_id,n_dict)
    list1=[]
    list1.append(update_net)
    update_subnet = conn.network.update_subnet(subnet_id,sn_dict)
    list2=[]
    list2.append(update_subnet)
    list = extract_network(list1,list2)
    return list



def find_network(conn,network_id):
    network = conn.network.find_network(network_id)
    print 'The network we find is'+ network
    return network.to_dict





# A router is a logical component that forwards data packets between networks.
# It also provides Layer 3 and NAT forwarding to provide external network access for servers on project networks.
def list_routers(conn):
    routers = conn.network.routers()
    list =[]
    for router in routers:
        list.append(router.to_dict)
        # list.append(extract_router(router))
    return list


    # openstack.network.v2.router.Router(attrs={u'status': u'ACTIVE',
        #                                       u'external_gateway_info': {
                                    #                                       u'network_id': u'4e9b7eea-fcd3-4773-bcb4-711b44979b18',
                                    #                                       u'enable_snat': True,
                                    #                                       u'external_fixed_ips': [{u'subnet_id': u'ce500f45-b8f9-42fa-a9e5-cd31b04b4822',
                                    #                                                               u'ip_address': u'202.112.113.229'}]},
                                    #                                       u'name': u'router-qll',
                                    #                                       u'admin_state_up': True,
                                    #                                       u'tenant_id': u'02d5ad020bec441185dd901f61cb28db',
                                    #                                       u'distributed': False,
                                    #                                       u'routes': [],
                                    #                                       u'ha': False,
                                    #                                       u'id': u'f48c689d-3fe2-4e5e-ac9e-5b2f4a28cca1'},
        #                               loaded=True)


# openstack.network.v2.router.Router(attrs={u'status': u'ACTIVE',
                                            # u'external_gateway_info': {u'network_id': u'4e9b7eea-fcd3-4773-bcb4-711b44979b18',
                                            #                            u'enable_snat': True,
                                            #                            u'external_fixed_ips': [{u'subnet_id': u'ce500f45-b8f9-42fa-a9e5-cd31b04b4822',
                                            #                                                     u'ip_address': u'202.112.113.231'}]},
                                            #                           u'name': u'admin-router',
                                            #                           u'admin_state_up': True,
                                            #                           u'tenant_id': u'2f1bc8c34f094d049a201819732537a3',
                                            #                           u'distributed': False,
                                            #                           u'routes': [],
                                            #                           u'ha': False,
                                            #                           u'id': u'3f597b1f-f34c-41e7-bd1e-81321371545f'},
#                                           loaded=True)


#/*****************************************************************/
# create_router(**attrs)
# Create a new router from attributes
# Parameters:attrs (dict)- Keyword arguments which will be used to create a Router, comprised of the properties on
# the Router class.
# Returns:	The results of router creation
# Return type:	Router
#/*****************************************************************/
def create_router(conn,router_name,external_net_name):
    new_router = conn.network.create_router(router_name,external_net_name)
    router_dict = extract_router(new_router)
    return new_router


def delete_router(conn,router_id):
    conn.network.delete_router(router_id,ignore_missing=False)


def update_router(conn,router_id):
    update_router = conn.network.update_router(router_id)
    return update_router


def get_router(conn,router_id):
    router = conn.network.get_router(router_id)
    return router

def find_router(conn,router_id):
    router = conn.network.find_router(router_id,ignore_missing=False)
    return router

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
def add_gateway_to_router(conn,router_id,public_net_name):
    print 'Add the router to public net'
    router = conn.network.add_gateway_to_router(router_id,public_net_name)
    # router_dict = extract_router(router)
    return router.to_dict

# remove_gateway_from_router(router, **body)
# Remove Gateway from a router
#
# Parameters:
# router-Either the router ID or an instance of Router
# body - Body with the gateway information
# Returns:
# Router with updated interface
#
# Return type:
# class:	~openstack.network.v2.router.Router
def remove_gateway_from_router(conn,router_id,public_net_name):
    print 'Remove the router to public net'
    router = conn.network.remove_gateway_to_router(router_id,public_net_name)
    # router_dict = extract_router(router)
    return router.to_dict


#add_interface_to_router(router, subnet_id=None, port_id=None)
# Add Interface to a router
#
# Parameters:
# router -Either the router ID or an instance of Router
# subnet_id -ID of the subnet
# port_id -ID of the port
# Returns:
# Router with updated interface
#
# Return type:
# class:	~openstack.network.v2.router.Router
def add_interface_to_router(conn,router_id,subnet_id,port_id=None):
    print 'Add the subnet to router'
    router = conn.network.add_interface_to_router(router_id,subnet_id=None,port_id=None)
    # router_dict = extract_router(router)
    return router.to_dict


def remove_interface_from_router(conn,router_id,subnet_id,port_id=None):
    print 'Remove the subnet to router'
    router = conn.network.remove_interface_to_router(router_id,subnet_id=None,port_id=None)
    # router_dict = extract_router(router)
    return router.to_dict


#***********************Auto Allocated Topology Operations******************/
def delete_auto_allocated_topology(conn,project_id, ignore_missing=False):
    conn.network.delete_auto_allocated_topology(project_id=None, ignore_missing=False)

def get_auto_allocated_topology(conn,project_id):
    topo = conn.network.get_auto_allocated_topology(project_id=None)
    return topo.to_dict

def validate_auto_allocated_topology(conn,project_id):
    validate_topo = conn.network.validate_auto_allocated_topology(project_id=None)
    return validate_topo.to_dict




