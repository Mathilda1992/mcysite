#mcy update in 2017-1-4
# this file is used to create forms,just like we create Models in models.py

from django import forms



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



class AddExpForm(forms.Form):
    name = forms.CharField(label='name')
    desc = forms.CharField(label='desc',widget=forms.Textarea(),required =False)






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

)

class AddDeliveryForm(forms.Form):
    name = forms.CharField(label='name',required=True,max_length=50,
                           error_messages={'required': 'The delivery can not be null!','max_length':'The delivery name is too long'})
    desc = forms.CharField(label='Gdesc', max_length=500, widget=forms.Textarea(), required=False,
                           initial="Replace with your description",
                           error_messages={'max_length': 'The description is too long'})
    exp = forms.MultipleChoiceField(label='exp',required=True,widget=forms.CheckboxSelectMultiple,choices=EXP_CHECKBOX_CHOICES,)
    group = forms.MultipleChoiceField(label="group",required=True,widget=forms.CheckboxSelectMultiple,choices=GROUP_CHECKBOX_CHOICES,)
    startDate = forms.DateField(label='starttime',widget=forms.SelectDateWidget(years=EXP_YEAR_CHOICES))
    endDate = forms.DateField(label='endtime', widget=forms.SelectDateWidget(years=EXP_YEAR_CHOICES))




