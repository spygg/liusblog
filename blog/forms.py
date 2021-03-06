from django import forms
from django.contrib import auth 
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}) )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username = username, password=password)

        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=3, widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30用户名'}))
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    verify_code = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入验证码'}))
    password = forms.CharField(min_length = 6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(min_length = 6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再次输入密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_verify_code(self):
        code = self.request.session.get('verify_code', '')
        verify_code = self.cleaned_data.get('verify_code', '')

        if code != verify_code:
            raise forms.ValidationError('验证码错误!')
            
        return self.cleaned_data;

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

       

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']

        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致')

        return password


class ResetPassWdForm(forms.Form):
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email