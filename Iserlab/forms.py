#mcy update in 2017-1-4
# this file is used to create forms,just like we create Models in models.py

from django import forms
import datetime


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

class AddExpForm(forms.Form):
    name = forms.CharField(label='Exp Name')
    desc = forms.CharField(label='Description',
                           widget=forms.Textarea(),
                           required =False)
    images_idList = forms.MultipleChoiceField(label='Include Images',
                                       widget=forms.CheckboxSelectMultiple,
                                       choices=IMAGES_CHECKBOX_CHOICES,)
    networks_idList = forms.MultipleChoiceField(label='Use Networks',
                                         widget=forms.CheckboxSelectMultiple,
                                         choices=NETWORKS_CHECKBOX_CHOICES,)
    # shared = forms.BooleanField(label='Share to Public Repo',
    #                             initial=False,)
    # guide = forms.FileField(label="Upload Guide",
    #                         widget=forms.ClearableFileInput(),
    #                         )
    guide = forms.CharField(label="Guide",
                            widget=forms.Textarea(),
                            required = False)
    refer_result = forms.CharField(label="Refer Result",
                                   widget=forms.Textarea(),
                                   required=False,)


class EditExpForm(forms.Form):# the same with AddExpForm
    pass


class SubmitExpForm(forms.Form):
    pass



class CreateImageForm(forms.Form):
    name =forms.CharField(label='Image Name')
    desc = forms.CharField(label='Description', widget=forms.Textarea(), required=False)
    imageUrl = forms.URLField(label='Image Download URL',required=False,initial='http://')
    imageFile = forms.ImageField(label='Upload Local Image File',)



class AddNetworkForm(forms.Form):
    pass


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

EXP_CHECKBOX_CHOICES=(
    ('24','exp00000'),
    ('21','new_create_exp444')
)

GROUP_CHECKBOX_CHOICES=(
    ('17','class111qqqqq0000'),
    ('15','group4'),
    ('13','group3'),
    ('4','group1'),
)

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
                                    widget=forms.CheckboxSelectMultiple,
                                    choices=EXP_CHECKBOX_CHOICES,)
    group = forms.MultipleChoiceField(label="Select Group",
                                      widget=forms.CheckboxSelectMultiple,
                                      choices=GROUP_CHECKBOX_CHOICES,)
    startDateTime = forms.DateField(label='Starttime',
                                    widget=forms.SelectDateWidget,
                                    initial=datetime.datetime.now())
    endDateTime = forms.DateField(label='Endtime',
                                  widget=forms.SelectDateWidget,
                                  initial=datetime.datetime.now()
                                  )

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
                                      choices=GROUP_CHECKBOX_CHOICES, )
    startDateTime = forms.DateField(label='Starttime',
                                    widget=forms.SelectDateWidget,
                                    )
    endDateTime = forms.DateField(label='Endtime',
                                  widget=forms.SelectDateWidget,
                                  )

