from extract_openstack_data import *


def create_connection(auth_url, region, project_name, username, password):
    conn = connection.Connection(
        # profile=prof,
        user_agent='IserLab',
        auth_url=auth_url,
        region=region,
        project_name=project_name,
        username=username,
        password=password
    )
    return conn


def image_list():
    # create conn to openstack
    conn = create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    # define sth used to deliver to html
    ImageList = []
    # get images data from openstack
    images = list_images(conn)
    for image in images:
        pass
    # print type(images);
    print images.next()
    for image in images:
        print image
    print('**********List Images**************')
    print images
    imagelist = extractimage(images)


def network_list():
    # create conn to openstack
    conn = create_connection(auth_url, region_name, project_name, auth_username, auth_password)

    NetworkList = []

    networks = list_networks(conn)

    NetworkList = extractnetwork(networks)

    for i in range(0, len(NetworkList)):
        # print NetworkList[i];
        print NetworkList[i]["attrs"]["subnets"]


def list_subnet():
    conn = create_connection(auth_url, region_name, project_name, auth_username, auth_password)
    return conn.network.subnets();


def subnet_list():
    print("List Subnet:")
    subnets = list_subnet();
    SubnetsList = extractnetwork(subnets);
    # print SubnetsList
    # for item in SubnetsList:
    # `print item
    for i in range(0, len(SubnetsList)):
        print SubnetsList[i]["attrs"]["start"]
        print SubnetsList[i]["attrs"]["end"]
        # print item
        # print type(item);
        # print item["attrs"]["gateway_ip"]
        # print item[0]["attrs"]["gateway_ip"];
