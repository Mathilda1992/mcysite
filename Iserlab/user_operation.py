#mcy update in 2017-1-3


from Iserlab.models import User,Group,Student
from Iserlab import identity_resource_operation






#----------------------------pass this function---------------------------------#
##for openstack api error reason, this function not to do
def create_user(name,ps,role,email='',):
    #insert into User db
    if role == "teacher":
        u = User(username=name,password=ps,email=email)
    else:
        u = Student(stu_username=name,stu_password=ps,stu_email=email)
    u.save()

    return u
#----------------------------pass this function---------------------------------#

#list all user(teacher) info in system db table
def list_user():
    u_list = User.objects.all()
    return u_list



def find_user(name):
    u = User.objects.get(username = name)
    # u_dict = {'username':u.username,'password':u.password,'email':u.email}
    # print u_dict
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

def list_group(teacher):
    print teacher
    g_list = Group.objects.filter(teacher = teacher)
    print g_list
    print g_list[0].name
    print g_list[0].stuCount
    return g_list

#------attr for group object-----
#['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', u'__module__',
# '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_base_manager',
# '_check_column_name_clashes', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_local_fields', '_check_long_column_names',
# '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_ordering', '_check_swappable', '_check_unique_together', '_default_manager', '_deferred',
# '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks',
# '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', 'check', 'clean', 'clean_fields', 'created_at', 'date_error_message', 'delete', 'delivery_set', 'desc',
#  'from_db', 'full_clean', 'get_deferred_fields', 'get_next_by_created_at', 'get_previous_by_created_at', 'id', 'name', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save',
# 'save_base', 'serializable_value', 'stuCount', 'student', 'teacher', 'teacher_id', 'unique_error_message', 'validate_unique']




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
        s_dict = {'id':s.id,'stu_username':s.stu_username,'stu_password':s.stu_password,'stu_email':s.stu_email}
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

#----attr for student object
#['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', u'__module__',
# '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_base_manager',
# '_check_column_name_clashes', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_local_fields', '_check_long_column_names',
# '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_ordering', '_check_swappable', '_check_unique_together', '_default_manager', '_deferred',
# '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks',
#  '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean',
# 'get_deferred_fields', 'group_set', 'id', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'stu_email', 'stu_password',
# 'stu_username', 'unique_error_message', 'validate_unique']



def add_stu_group(g_name,stulist):
    g = Group.objects.get(name=g_name)
    for stu in stulist:
        g.student.add(stu)




def remove_stu_group(g_name,stulist):
    g = Group.objects.get(name=g_name)
    for stu in stulist:
        g.student.remove(stu)


