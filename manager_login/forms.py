from django import forms

class LoginForm(forms.Form):
    email_or_username = forms.CharField(label='Email or Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)