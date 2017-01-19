from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

def create_conn():
    #set conn argus
    auth_username = 'admin'
    auth_password = 'os62511279'
    auth_url = 'http://202.112.113.220:5000'
    project_name = 'admin'
    region_name = 'RegionOne'

    provider = get_driver(Provider.OPENSTACK)
    conn = provider(auth_username,
                    auth_password,
                    ex_force_auth_url=auth_url,
                    ex_force_auth_version='2.0_password',
                    ex_tenant_name=project_name,
                    ex_force_service_region=region_name)
    return conn;