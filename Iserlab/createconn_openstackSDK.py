#mcy update 2016-12-05
#from openstack import profile
from openstack import connection



def create_connection(auth_url, region, project_name, username, password):
    #prof = profile.Profile()
    #prof.set_region(profile.Profile.ALL, region)

    conn = connection.Connection(
        #profile=prof,
        user_agent='IserLab',
        auth_url=auth_url,
        region=region,
        project_name=project_name,
        username=username,
        password=password
    )
    return conn