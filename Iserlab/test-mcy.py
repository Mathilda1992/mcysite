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