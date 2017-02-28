#mcy update 2016-12-05
#all data are in openstack level
#Refer to:http://developer.openstack.org/sdks/python/openstacksdk/users/proxies/image.html#image-api-v2


from extract_openstack_data import *

def extract_image(images):
    list = []
    for item in images:
        dict = {}
        print item.allow_create
        dict.setdefault("add_tag",item.add_tag)
        dict.setdefault("allow_create",item.allow_create)
        dict.setdefault("allow_delete",item.allow_delete)
        dict.setdefault("allow_get",item.allow_get)
        dict.setdefault("allow_head",item.allow_head)
        dict.setdefault("allow_list",item.allow_list)
        dict.setdefault("allow_update",item.allow_update)
        dict.setdefault("architecture",item.architecture)
        dict.setdefault("base_path",item.base_path)
        dict.setdefault("checksum",item.checksum)#
        dict.setdefault("container_format", item.container_format)#
        dict.setdefault("create",item.create)
        dict.setdefault("created_at", item.created_at)#
        dict.setdefault("data",item.data)
        dict.setdefault("deactivate",item.deactivate)
        dict.setdefault("delete",item.delete)
        dict.setdefault("direct_url",item.direct_url)
        dict.setdefault("disk_format", item.disk_format)#
        dict.setdefault("download",item.download)
        dict.setdefault("existing",item.existing)
        dict.setdefault("file", item.file)#
        dict.setdefault("find",item.find)
        dict.setdefault("get",item.get)
        dict.setdefault("has_auto_disk_config",item.has_auto_disk_config)
        dict.setdefault("head",item.head)
        dict.setdefault("hw_cpu_cores",item.hw_cpu_cores)
        dict.setdefault("hw_cpu_sockets",item.hw_cpu_sockets)
        dict.setdefault("hw_cpu_threads",item.hw_cpu_threads)
        dict.setdefault("hw_disk_bus",item.hw_disk_bus)
        dict.setdefault("hw_machine_type",item.hw_machine_type)
        dict.setdefault("hw_rng_model",item.hw_rng_model)
        dict.setdefault("hw_scsi_model",item.hw_scsi_model)
        dict.setdefault("hw_serial_port_count",item.hw_serial_port_count)
        dict.setdefault("hw_video_model",item.hw_video_model)
        dict.setdefault("hw_video_ram",item.hw_video_ram)
        dict.setdefault("hw_vif_model",item.hw_vif_model)
        dict.setdefault("hw_watchdog_action",item.hw_watchdog_action)
        dict.setdefault("hypervisor_type",item.hypervisor_type)
        dict.setdefault("id", item.id)#
        dict.setdefault("instance_type_rxtx_factor",item.instance_type_rxtx_factor)
        dict.setdefault("instance_uuid",item.instance_uuid)##
        dict.setdefault("is_hw_boot_menu_enabled",item.is_hw_boot_menu_enabled)
        dict.setdefault("is_hw_vif_multiqueue_enabled",item.is_hw_vif_multiqueue_enabled)
        dict.setdefault("is_protected", item.is_protected)
        dict.setdefault("kernel_id",item.kernel_id)
        dict.setdefault("list",item.list)
        dict.setdefault("location",item.location)
        dict.setdefault("locations",item.locations)
        dict.setdefault("metadata",item.metadata)
        dict.setdefault("min_disk", item.min_disk)#
        dict.setdefault("min_ram", item.min_ram)#
        dict.setdefault("name", item.name)#
        dict.setdefault("needs_config_drive",item.needs_config_drive)
        dict.setdefault("needs_secure_boot",item.needs_secure_boot)
        dict.setdefault("new",item.new)
        dict.setdefault("os_command_line",item.os_command_line)
        dict.setdefault("os_distro",item.os_distro)
        dict.setdefault("os_type",item.os_type)
        dict.setdefault("os_version",item.os_version)
        dict.setdefault("owner_id", item.owner_id)#
        dict.setdefault("patch_update",item.patch_update)
        dict.setdefault("path",item.path)
        dict.setdefault("properties",item.properties)
        dict.setdefault("put_create",item.put_create)
        dict.setdefault("ramdisk_id",item.ramdisk_id)
        dict.setdefault("reactivate",item.reactivate)
        dict.setdefault("remove_tag",item.remove_tag)
        dict.setdefault("resource_key",item.resource_key)
        dict.setdefault("resources_key",item.resources_key)
        dict.setdefault("service",item.service)
        dict.setdefault("size", item.size)#
        dict.setdefault("status", item.status)#
        dict.setdefault("store",item.store)
        dict.setdefault("tags", item.tags)#
        # dict.setdefault("to_dict", item.to_dict)
        dict.setdefault("update",item.update)
        dict.setdefault("updated_at", item.updated_at)
        dict.setdefault("upload",item.upload)
        dict.setdefault("url",item.url)
        dict.setdefault("value",item.value)
        dict.setdefault("virtual_size", item.virtual_size)#
        dict.setdefault("visibility", item.visibility)#
        dict.setdefault("vm_mode",item.vm_mode)
        dict.setdefault("vmware_adaptertype",item.vmware_adaptertype)
        dict.setdefault("vmware_ostype",item.vmware_ostype)

        list.append(dict)
    return list

    # -----------result of dir(image): all attrs of Image object-----------------------------
    #['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__',
    # '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_action', '_alternate_id', '_body', '_body_mapping', '_collect_attrs', '_consume_attrs',
    # '_filter_component', '_get_id', '_get_mapping', '_get_one_match', '_header', '_header_mapping', '_prepare_request', '_query_mapping', '_translate_response', '_update', '_uri',
    # '_uri_mapping', 'add_tag', 'allow_create', 'allow_delete', 'allow_get', 'allow_head', 'allow_list', 'allow_update', 'architecture', 'base_path', 'checksum', 'container_format',
    # 'create', 'created_at', 'data', 'deactivate', 'delete', 'direct_url', 'disk_format', 'download', 'existing', 'file', 'find', 'get', 'has_auto_disk_config', 'head', 'hw_cpu_cores',
    # 'hw_cpu_sockets', 'hw_cpu_threads', 'hw_disk_bus', 'hw_machine_type', 'hw_rng_model', 'hw_scsi_model', 'hw_serial_port_count', 'hw_video_model', 'hw_video_ram', 'hw_vif_model',
    # 'hw_watchdog_action', 'hypervisor_type', 'id', 'instance_type_rxtx_factor', 'instance_uuid', 'is_hw_boot_menu_enabled', 'is_hw_vif_multiqueue_enabled', 'is_protected', 'kernel_id',
    # 'list', 'location', 'locations', 'metadata', 'min_disk', 'min_ram', 'name', 'needs_config_drive', 'needs_secure_boot', 'new', 'os_command_line', 'os_distro', 'os_type', 'os_version',
    # 'owner_id', 'patch_update', 'path', 'properties', 'put_create', 'ramdisk_id', 'reactivate', 'remove_tag', 'resource_key', 'resources_key', 'service', 'size', 'status', 'store', 'tags',
    # 'to_dict', 'update', 'updated_at', 'upload', 'url', 'value', 'virtual_size', 'visibility', 'vm_mode', 'vmware_adaptertype', 'vmware_ostype']

def list_images(conn):
    print("List Images:")
    images = conn.image.images()
    for image in conn.image.images():
        print(image)
        #print dir(image)
    #output result******
    #snapshot type data
    #openstack.image.v2.image.Image(status=active,
                                    # instance_uuid=89f2ef4f-8eab-4cce-bf59-5f19cb613b20,
                                    # name=admin-new-cirros-sp,
                                    # tags=[],
                                    # kernel_id=None,
                                    # container_format=bare,
                                    # min_ram=0,
                                    # ramdisk_id=None,
                                    # disk_format=qcow2,
                                    # updated_at=2017-02-21T03:09:41Z,
                                    # visibility=public,
                                    # min_disk=1,
                                    # protected=False,
                                    # file=/v2/images/5d3b53a3-b21e-4994-909c-2e3fc510e24f/file,
                                    # checksum=428008ea6b337729b09ed3761d5a7b1d,
                                    # owner=2f1bc8c34f094d049a201819732537a3,
                                    # created_at=2017-02-21T02:57:21Z,
                                    # virtual_size=None,
                                    # id=5d3b53a3-b21e-4994-909c-2e3fc510e24f,
                                    # size=22085632)
    #image type data
    #openstack.image.v2.image.Image(status=active,
                                    # created_at=2017-01-19T13:03:56Z,
                                    # name=win7_csdn,
                                    # tags=[],
                                    # container_format=bare,
                                    # min_ram=0,
                                    # disk_format=qcow2,
                                    # updated_at=2017-01-19T13:06:20Z,
                                    # visibility=public,
                                    # owner=2f1bc8c34f094d049a201819732537a3,
                                    # protected=False,
                                    # file=/v2/images/8cf204a7-cc69-4cf0-ada0-bdf1d0516e7c/file,
                                    # checksum=57f34b11fbe45b04c8e165e33d3e0517,
                                    # min_disk=0,
                                    # virtual_size=None,
                                    # id=8cf204a7-cc69-4cf0-ada0-bdf1d0516e7c,
                                    # size=7959805952)



    #extract the image data to a dict list
    list = extract_image(images)
    print "output data after extract!"
    for i in list:
        print i
    return list



def upload_image(conn,image_name):
    print("Upload Image:")

    # Load fake image data for the example.
    data = 'This is fake image data.'

    # Build the image attributes and upload the image.
    image_attrs = {
        'name': image_name,
        'data': data,
        'disk_format': 'raw',
        'container_format': 'bare',
        'visibility': 'public',
    }
    conn.image.upload_image(**image_attrs)
    return 0


def delete_image(conn,image_ID):
    print("Delete Image:")

    example_image = conn.image.find_image(image_ID)

    conn.image.delete_image(example_image, ignore_missing=False)
    return 0