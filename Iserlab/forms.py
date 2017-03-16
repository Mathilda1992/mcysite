#mcy update in 2017-1-4
# this file is used to create forms,just like we create Models in models.py

from django import forms
import datetime
from Iserlab.models import *


TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)


class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField()
    sender = forms.EmailField(required = False)




class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()



IMAGES_CHECKBOX_CHOICES=(
    ('1','cirros'),
    ('3','cirros-111'),
)

NETWORKS_CHECKBOX_CHOICES=(
    ('1','private_alice'),
    ('2','private_exp1'),
)

FLAVOR_CHOICE_BOX=(
    ('m1.tiny', 'm1.tiny(RAM=512MB,Disk=1GB,VCPUs=1)'),
    ('m1.small', 'm1.small(RAM=2048MB,Disk=20GB,VCPUs=1)'),
    ('m1.medium', 'm1.medium(RAM=4096MB,Disk=40GB,VCPUs=2)'),
    ('m1.large', 'm1.large(RAM=8192MB,Disk=80GB,VCPUs=4)'),
    ('m1.xlarge', 'm1.xlarge(RAM=16384MB,Disk=160GB,VCPUs=8)'),
)
KEYPAIR_CHOICE_BOX=(
    ('mykey','mykey'),
)
SECURITY_GROUP_CHOICE_BOX=(
    ('default','default'),
)
class AddVMForm(forms.Form):
    name = forms.CharField(label='VM name',max_length=150)
    desc = forms.CharField(label='Description',max_length=500,
                           widget=forms.Textarea(),
                           required =False)
    image_id = forms.ChoiceField(label='Include Images',)
    network_id = forms.ChoiceField(label='Use Networks',)
    flavor = forms.ChoiceField(label='Flavor',
                               widget=forms.RadioSelect(),
                               choices=FLAVOR_CHOICE_BOX,)
    keypair = forms.ChoiceField(label='Keypair',
                                widget=forms.RadioSelect(),
                                choices=KEYPAIR_CHOICE_BOX,)
    security_group = forms.MultipleChoiceField(label='Security Groups',
                                               widget=forms.CheckboxSelectMultiple,
                                               choices=SECURITY_GROUP_CHOICE_BOX,)

    def __init__(self,*args,**kwargs):
        super(AddVMForm,self).__init__(*args,**kwargs)
        # t= self.get_currentuser(request)
        self.fields['image_id'].choices = [(i.pk,str(i)) for i in ImageCart.objects.all()]
        self.fields['network_id'].choices = [(i.pk,str(i)) for i in NetworkCart.objects.all()]

    def get_currentuser(self,request):
        username = request.session['username']
        t = User.objects.get(username=username)
        return t



class AddExpForm(forms.Form):
    name = forms.CharField(label='Exp Name',max_length=150)
    desc = forms.CharField(label='Description',max_length=500,
                           widget=forms.Textarea(),
                           required =False)

    images_idList = forms.MultipleChoiceField(label='Include Images',
                                       # widget=forms.CheckboxSelectMultiple,
                                       )
    networks_idList = forms.MultipleChoiceField(label='Use Networks',
                                         # widget=forms.CheckboxSelectMultiple,
                                         )
    vm_count = forms.IntegerField(label="VM Count")
    vm_idList = forms.MultipleChoiceField(label='Include VMs',)
    guide = forms.CharField(label="Guide",
                            widget=forms.Textarea(),
                            required = False)
    guide_file = forms.FileField(label='Upload Guide File', required=True)
    refer_result = forms.CharField(label="Refer Result",
                                   widget=forms.Textarea(),
                                   required=False,)

    def __init__(self,*args,**kwargs):
        super(AddExpForm,self).__init__(*args,**kwargs)
        # t= self.get_currentuser(request)
        self.fields['images_idList'].choices = [(i.pk,str(i)) for i in ImageCart.objects.all()]
        self.fields['networks_idList'].choices = [(i.pk,str(i)) for i in NetworkCart.objects.all()]
        self.fields['vm_idList'].choices = [(i.pk,str(i)) for i in VM.objects.all()]


    def get_currentuser(self,request):
        username = request.session['username']
        t = User.objects.get(username=username)
        return t


class EditExpForm(forms.Form):# the same with AddExpForm
    pass




class SubmitExpForm(forms.Form):#actually equal to update Score table
    # name = forms.CharField(label="Exp Name",max_length=150,
    #                        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    result = forms.CharField(label="Result",widget=forms.Textarea(),required=False)
    reportFile = forms.FileField(label='Upload Report', required=True)



class CreateImageForm(forms.Form):
    name =forms.CharField(label='Image Name',max_length=255)
    desc = forms.CharField(label='Description', widget=forms.Textarea(), required=False)
    myfile = forms.FileField(label='Upload Local Image File',required=True)
    # imageUrl = forms.URLField(label='Image Download URL',required=False,initial='http://')
    # imageFile = forms.ImageField(label='Upload Local Image File',required=True)

class EditImageForm(forms.Form):
    name = forms.CharField(label='Image name',max_length=255)
    desc = forms.CharField(label='Description',widget=forms.Textarea(),required=False)


class AddNetworkForm(forms.Form):
    name = forms.CharField(label = "Network Name",max_length=100)
    subnet_name =forms.CharField(label='Subnet Name',max_length=50)
    desc = forms.CharField(label = 'Description',widget=forms.Textarea(),required=False)
    ip_version = forms.CharField(label='IP Version',max_length=2)
    cidr = forms.CharField(label='CIDR',max_length=40)
    gateway = forms.CharField(label='Gateway IP',max_length=50)
    allocation_pools_start =forms.CharField(label='allocation_pools_start',max_length=30)
    allocation_pools_end=forms.CharField(label='allocation_pools_end',max_length=30)
    enable_dhcp = forms.BooleanField(label='Enable DHCP',)



#define report upload form for student
class UploadFileForm(forms.Form):
    title = forms.CharField(label='Title',max_length=50)
    file = forms.FileField(label='Upload Report',)


#define score form for teacher
class ScoreForm(forms.Form):
    score = forms.DecimalField(label='Score',
                               required=True,
                               max_value=100.00,
                               min_value=0.00,
                               max_digits=5,
                               error_messages={'required': 'You must give a score.',
                                               'invalid': 'Please input a decimal format value.',
                                               'max_value': 'Please give a value less then 100.00.',
                                               'min_value': 'Please give a value bigger than 0.00.',
                                               'max_digits': 'Please give a value within 5 digits.'})
    comment = forms.CharField(label='Comment',max_length=500,
                              required=False,
                              widget=forms.Textarea(),
                              )




#delivery form
EXP_YEAR_CHOICES=('2017','2018','2019')





class AddDeliveryForm(forms.Form):
    name = forms.CharField(label='Delivery Name',
                           max_length=50,
                           error_messages={'required': 'The delivery can not be null!','max_length':'The delivery name is too long'})
    desc = forms.CharField(label='Description', max_length=500,
                           widget=forms.Textarea(),
                           required=False,
                           initial="Replace with your description",
                           error_messages={'max_length': 'The description is too long'})

    exp = forms.MultipleChoiceField(label='Select Exp',
                                    widget=forms.CheckboxSelectMultiple, )
    group = forms.MultipleChoiceField(label="Select Group",
                                      widget=forms.CheckboxSelectMultiple,
                                      )
    startDateTime = forms.DateField(label='Starttime',
                                    widget=forms.SelectDateWidget,
                                    initial=datetime.datetime.now())
    endDateTime = forms.DateField(label='Endtime',
                                  widget=forms.SelectDateWidget,
                                  initial=datetime.datetime.now()
                                  )

    def __init__(self,*args,**kwargs):
        super(AddDeliveryForm,self).__init__(*args,**kwargs)
        # t= self.get_currentuser(request)
        self.fields['exp'].choices = [(i.pk,str(i)) for i in Experiment.objects.all()]
        self.fields['group'].choices = [(i.pk,str(i)) for i in Group.objects.all()]


    def get_currentuser(self,request):
        username = request.session['username']
        t = User.objects.get(username=username)
        return t


class EditDeliveryForm(forms.Form):
    name = forms.CharField(label='Delivery Name',
                           max_length=50,
                           error_messages={'required': 'The delivery can not be null!',
                                           'max_length': 'The delivery name is too long'})
    desc = forms.CharField(label='Description', max_length=500,
                           widget=forms.Textarea(),
                           required=False,
                           initial="Replace with your description",
                           error_messages={'max_length': 'The description is too long'})
    exp = forms.CharField(label='Experiment',max_length=150,
                          widget=forms.TextInput(attrs={'readonly':'readonly'}),)
    group = forms.CharField(label='Group',max_length=50,
                            widget=forms.TextInput(attrs={'readonly': 'readonly'}),)
    startDateTime = forms.DateField(label='Starttime',
                                    widget=forms.SelectDateWidget,
                                    )
    endDateTime = forms.DateField(label='Endtime',
                                  widget=forms.SelectDateWidget,
                                  )


class ExpDeliveryForm(forms.Form):
    name = forms.CharField(label='Delivery Name',
                           max_length=50,
                           error_messages={'required': 'The delivery can not be null!',
                                           'max_length': 'The delivery name is too long'})
    desc = forms.CharField(label='Description', max_length=500,
                           widget=forms.Textarea(),
                           required=False,
                           initial="Replace with your description",
                           error_messages={'max_length': 'The description is too long'})

    group = forms.MultipleChoiceField(label="Select Group",
                                      widget=forms.CheckboxSelectMultiple,
                                      )
    startDateTime = forms.DateField(label='Starttime',
                                    widget=forms.SelectDateWidget,
                                    )
    endDateTime = forms.DateField(label='Endtime',
                                  widget=forms.SelectDateWidget,
                                  )

    def __init__(self,*args,**kwargs):
        super(ExpDeliveryForm,self).__init__(*args,**kwargs)
        self.fields['group'].choices = [(i.pk,str(i)) for i in Group.objects.all()]