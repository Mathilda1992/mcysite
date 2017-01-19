#mcy update in 2016-12-20
#Here are some operations related to the repo-- image repo
#The template repo operation already in the experiment_resource_operation.py

#data in system level(integrate with db:VMImage)

from Iserlab.models import VMImage,Network

def list_VMImage(image_name):
    print('List images in repo:')
    ilist = []
    ilist = VMImage.objects.all()
    for i in ilist:
        print i
    return ilist


def get_VMImage(image_name):
    print('Get image in repo by name:')
    i = VMImage.objects.get(name = image_name)
    print i
    return i


def add_VMImage():
    pass



def delete_VMImage():
    pass

def modify_VMImage():
    pass



#data in system level(integrate with db:Network)
def list_network():
    print('List netwoks in Repo:')
    nlist = []
    nlist = Network.objects.all()
    for i in nlist:
        print i
    return nlist

def get_network(name):
    print('Get network in Repo:')
    n = Network.objects.get(network_name=name)
    print n
    return n

def add_network():
    pass

def delete_network():
    pass


def modify_netwokr():
    pass
