#mcy update in 2017-1-3


from Iserlab.models import User,Group,Student
from Iserlab import identity_resource_operation



#list all user info in system db table
def list_user():
    u_list = User.objects.all()
    return u_list


##for openstack api error reason, this function not to do
def create_user(name,ps,email=''):
    #insert into User db
    u = User(username=name,password=ps,email=email)
    u.save()
    #create openstack user

    # get the domain

    # create project

    # create user

    # get role

    # add role to project and user

    return u


def find_user(name):
    u = User.objects.get(username = name)
    u_dict = {'username':u.username,'password':u.password,'email':u.email}
    print u_dict
    return u



def delete_user(name):
    #delete the record in db
    User.objects.filter(username=name).delete()
    #delete the user in openstack

    pass



def update_user(name):
    pass



#********************************stu operation*******************************
def list_stu():
    pass


def create_stu(name,ps,email):
    pass

def find_stu(name):
    s = Student.objects.get(stu_username=name)
    return s


def delete_stu(name):
    pass


def update_stu(name):
    pass



#********************************group operation*******************************

def list_group():
    g_list = Group.objects.all()
    print g_list
    return g_list




def create_group(gname,gteacher,gcount,stulist,desc='Please input description'):
    g = Group(name=gname,desc=desc,teacher=gteacher,stuCount=gcount)
    g.save()

    for stu in stulist:
        g.student.add(stu)

    print g
    return g



def delete_group(g_name):
    g = Group.objects.filter(name = g_name).delete()



def view_group(g_name):
    g = Group.objects.get(name=g_name)
    #put info of group into a dict
    t = g.teacher

    t_dict = {'username': t.username, 'password': t.password, 'email': t.email}

    s_list = g.student.all()
    s_dict_list = []
    for s in s_list:
        s_dict = {'username':s.stu_username,'password':s.stu_password,'email':s.stu_email}
        s_dict_list.append(s_dict)

    g_dict = {'name':g_name ,'desc':g.desc,'teacher':t_dict,'stulist':s_dict_list,'stucount':g.stuCount}
    print g_dict
    return g_dict




def get_group(teacher):
    glist = Group.objects.filter(teacher = teacher)
    print glist
    return glist



def get_group_stu(g_name):
    g = Group.objects.get(name = g_name)
    stulist = g.student.all()
    print stulist
    return stulist



def add_stu_group(g_name,stulist):
    g = Group.objects.get(name=g_name)
    for stu in stulist:
        g.student.add(stu)




def remove_stu_group(g_name,stulist):
    g = Group.objects.get(name=g_name)
    for stu in stulist:
        g.student.remove(stu)


