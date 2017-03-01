from django import forms
class CommentForm(forms.Form):
    name = forms.CharField(label='username',max_length=16,error_messages={'required':'Please input your name','max_length':'The name is too long'})
    email = forms.EmailField(label='email',error_messages={'required':'Please input your email','invalid':'The format is wrong'})
    content = forms.CharField(label='content',max_length=100,error_messages={'required':'Please input your comment','max_length':'The comment is too long'})