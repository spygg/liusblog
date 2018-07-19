from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length = 30)
    password = forms.CharField(label='password', widget=forms.PasswordInput)