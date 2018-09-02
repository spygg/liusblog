from django import forms
from django.contrib import auth 
from django.contrib.auth.models import User

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'留下足迹再走嘛~'}))

    def clean(self):
        content = self.cleaned_data['content']
        # user = auth.authenticate(username = username, password=password)
        # if user is None:
        #     raise forms.ValidationError('用户名或密码错误')
        # else:
        #     self.cleaned_data['user'] = user
        return self.cleaned_data

