# Create your login here.

from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#from django.core.context_processors import csrf
from django import forms
from django.core.mail import send_mail

from .forms import *
from Iserlab.models import User,Student

from django.core.exceptions import ValidationError


def validate_username(username):
    if username =="badboy":
        raise ValidationError('%s is used, please change one!' % username)



system_admin_email = ['machenyi2011@163.com',]


# Define the form model for login

ROLE_CHOICES = (('teacher', 'Teacher Role'), ('student', 'Student Role'))
class LoginForm(forms.Form):
    username = forms.CharField(label='USERNAME', max_length=100,error_messages={'required': 'The username can not be null!'})
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(),error_messages={'required': 'The password can not be null!'})



class RegisterForm(forms.Form):
    username = forms.CharField(label='USERNAME', max_length=100,help_text="The username should be English letter or number!",error_messages={'required': 'The username can not be null!'},validators=[validate_username])
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(),error_messages={'required': 'The password can not be null!'})
    password_r = forms.CharField(label='PASSWORD REPEAT', widget=forms.PasswordInput())
    # email = forms.CharField(label='EMAIL', error_messages={'required': 'The email can not be null!'})
    email = forms.EmailField(label='EMAIL', error_messages={'required': 'The email can not be null!','invalid': 'Please input the correct email!'})
    role = forms.ChoiceField(label="ROLE", choices= ROLE_CHOICES,widget=forms.RadioSelect(),error_messages={'required': 'The role must be chosen!'})


    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data.get('password')
        password_r = cleaned_data.get('password_r')
        if password != password_r:
            self._errors['password']=self.error_class(['Different password!'])
        else:
            return cleaned_data


def login(request):
    if request.method == 'POST':
        uf = LoginForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            print username
            password = uf.cleaned_data['password']
            #compare with data from db to check whether the user login exists in db
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                #save the user in session
                print "log sucess!"
                request.session['username'] = username
                print request.user.username
                return render_to_response("home.html",{'username':username})
            else:
                print "username or password error!!!"
                return HttpResponseRedirect('/login/')
    else:#request.method == 'GET'
        uf = LoginForm()
        return render_to_response("login.html",{'uf':uf})



def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponse("You are logged out.")





def register(request):
    if request.method == 'POST':
        rf = RegisterForm(request.POST)
        if rf.is_valid():
            username = rf.cleaned_data['username']
            password = rf.cleaned_data['password']
            password_r = rf.cleaned_data['password_r']
            email = rf.cleaned_data['email']
            role = rf.cleaned_data['role']

            if password == password_r:
                #insert this record into db

                if role == "teacher":
                    u = User(username=username, password=password, email=email)
                    u.save()
                    user = User.objects.filter(username__exact=username, password__exact=password)
                else:
                    u = Student(stu_username=username, stu_password=password, stu_email=email)
                    u.save()
                    user = Student.objects.filter(stu_username__exact=username, stu_password__exact=password)

                if user:
                    # system should notify system_admin by email
                    #send_mail('Subject here', 'Here is the message', 'source_email', 'target_email_list', fail_silently=False)
                    send_mail('Apply for register','<Username>:'+username+'<Password>:'+password+'<Email>:'+email+'<Role>:'+role, 'machenyi2011@163.com',system_admin_email,fail_silently=False)

                    return render_to_response("login.html")
                else:
                    return HttpResponse("Register Failed!")
            else:
                print "Different Password!"
                return HttpResponse("Different Password!")
    else:
        rf = RegisterForm()
    return render_to_response("register.html",{'rf':rf})

