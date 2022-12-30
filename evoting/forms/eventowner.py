# eventowner.py --> Forms

from django import forms


class SignupForm(forms.Form):
    firstname = forms.CharField(label="First Name")
    lastname = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email")
    gender = forms.CharField(label="Gender", max_length=1)
    password = forms.CharField(label="Passowrd")
    repeat_password = forms.CharField(label="Re-Enter Password")
    otp = forms.IntegerField(label="OTP")


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Passowrd")
