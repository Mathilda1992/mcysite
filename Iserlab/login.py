# Create your login here.

from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#from django.core.context_processors import csrf
from django import forms
from Iserlab.models import User


#Define the form model
class UserForm(forms.Form):
    username = forms.CharField(label='USERNAME',max_length=100)
    password = forms.CharField(label='PASSWORD',widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label='USERNAME',max_length=100)
    password = forms.CharField(label='PASSWORD',widget=forms.PasswordInput())
    password_r = forms.CharField(label='PASSWORD REPEAT', widget=forms.PasswordInput())


def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
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
        uf = UserForm()
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

            if password == password_r:
                #insert this record into db
                insert1 = User(username = username,password = password)
                insert1.save()
                user = User.objects.filter(username__exact=username, password__exact=password)
                if user:
                    return HttpResponse("Register Success!")
                else:
                    return HttpResponse("Register Failed!")
            else:
                return HttpResponse("Different Password!")
    else:
        rf = RegisterForm()
        return render_to_response("register.html",{'rf':rf})

