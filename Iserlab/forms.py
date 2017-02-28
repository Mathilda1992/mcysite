#mcy update in 2017-1-4
# this file is used to create forms,just like we create Models in models.py

from django import forms



TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)



EXP_YEAR_CHOICES = ('2017','2018')


class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField()
    sender = forms.EmailField(required = False)


class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()










#delivery form
class DeliveryForm(forms.Form):
    exp = forms.CharField(label='EXP_NAME')
    group = forms.CharField(label="GROUP_NAME")
    startDate = forms.DateField(label='START',widget=forms.SelectDateWidget(years=EXP_YEAR_CHOICES))
    endDate = forms.DateField(label='END', widget=forms.SelectDateWidget(years=EXP_YEAR_CHOICES))

