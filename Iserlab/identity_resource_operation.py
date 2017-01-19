#mcy update 2016-12-05
#Refer to:http://developer.openstack.org/sdks/python/openstacksdk/users/proxies/identity.html#identity-api-v3


#/*****************************************List***********************************/
def list_users(conn):
    print("List Users:")

    for user in conn.identity.users():
        print(user)


def list_credentials(conn):
    print("List Credentials:")

    for credential in conn.identity.credentials():
        print(credential)


def list_projects(conn):
    print("List Projects:")

    for project in conn.identity.projects():
        print(project)


def list_domains(conn):
    print("List Domains:")

    for domain in conn.identity.domains():
        print(domain)


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


#/*****************************************Create***********************************/
def create_user(conn):
    pass
