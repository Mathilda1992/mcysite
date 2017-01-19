#mcy update 2016-12-05
#all data are in openstack level
#Refer to:http://developer.openstack.org/sdks/python/openstacksdk/users/proxies/image.html#image-api-v2


from extract_openstack_data import *



def list_images(conn):
    images = conn.image.images()
    # print("List Images:")
    # for image in conn.image.images():
    #     print(image)

    #output result******
    #openstack.image.v2.image.Image(status=active,
    #                               created_at=2016-12-08T11:06:47Z,
    #                               name=cirros-222,
    #                               tags=[],
    #                               container_format=bare,
    #                               min_ram=0,
    #                               disk_format=qcow2,
    #                               updated_at=2016-12-08T11:06:47Z,
    #                               visibility=private,
    #                               owner=bd9dc26b524143339cad03c0ee048429,
    #                               protected=False,
    #                               file=/v2/images/fe28ce5e-1567-4153-8a06-265d7dbb66a8/file,
    #                               checksum=ee1eca47dc88f4879d8a229cc70a07c6,
    #                               min_disk=0,
    #                               virtual_size=None,
    #                               id=fe28ce5e-1567-4153-8a06-265d7dbb66a8,
    #                               size=13287936)

    imageDictList = extractimage(images)
    print imageDictList
    return images



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