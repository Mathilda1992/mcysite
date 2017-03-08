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
    username = forms.CharField(label='USERNAME', max_length=100,
                               error_messages={'required': 'The username can not be null!'})
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(),
                               error_messages={'required': 'The password can not be null!'})



class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               help_text="The username should be English letter or number!",
                               error_messages={'required': 'The username can not be null!'},
                               validators=[validate_username])
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(),
                               error_messages={'required': 'The password can not be null!'})
    password_r = forms.CharField(label='Password Repeat',
                                 widget=forms.PasswordInput())
    # email = forms.CharField(label='EMAIL', error_messages={'required': 'The email can not be null!'})
    email = forms.EmailField(label='Email',
                             error_messages={'required': 'The email can not be null!',
                                             'invalid': 'Please input the correct email format!'})
    role = forms.ChoiceField(label="Role",
                             choices= ROLE_CHOICES,
                             widget=forms.RadioSelect(),
                             error_messages={'required': 'The role must be chosen!'})
    #----test use----

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
            #compare with data from db to check whether the user login exists in db(bothe teacher and student db)
            user = User.objects.filter(username__exact = username,password__exact = password)
            stu = Student.objects.filter(stu_username__exact=username,stu_password__exact=password)
            if user:
                print "Teacher log in!"

                #-------save the user in session
                request.session['username'] = username
                request.session['role']='teacher'

                # #request.user:this object means login user
                # if request.user.is_authenticated():
                #     print "*******"
                #     print "output the login user info:????Why the user is admin????"
                #     print request.user.username
                #     print request.user.password
                #     print request.user.last_login
                #     print request.user.date_joined
                # else:
                #     print "#######"
                return HttpResponseRedirect('/home/')


                # #--------set username into cookies
                # response = HttpResponseRedirect('/home/')
                # response.set_cookie('username',username)
                # response.set_cookie('role','teacher')
                # return response


            elif stu:
                print "Student log in"
                request.session['username'] = username
                request.session['role'] = 'sutdent'
                return HttpResponseRedirect('/home/')

            else:
                print "ERROR:username or password error!!!"
                return HttpResponseRedirect('/login/')


    else:#request.method == 'GET'
        uf = LoginForm()
    return render_to_response("login.html",{'uf':uf})



def logout(request):
    #-----use session
    try:
        #clear the session
        del request.session['username']
    except KeyError:
        pass
    return HttpResponse("You are logged out.")


    # #----use cookie
    # response = HttpResponse('logout!!')
    # response.delete_cookie('username')
    # return response




def register(request):
    if request.method == 'POST':
        rf = RegisterForm(request.POST)
        if rf.is_valid():
            #get data from form
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

                    return HttpResponseRedirect("/login/")

                else:
                    return HttpResponse("Register Failed!")
            else:
                return HttpResponse("Different Password!")
    else:
        rf = RegisterForm()

    return render_to_response("register.html",{'rf':rf})



