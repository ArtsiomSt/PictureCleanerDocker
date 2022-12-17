from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from .models import PictureForRecongition


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label='Password')


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(), label='Repeat password')


class ChangeUserProfileDataForm(forms.Form):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)


class SetNewPassword(SetPasswordForm):
    pass


class AddPictureForRecogintionForm(forms.Form):
    save_or_not = forms.BooleanField(label="Press here and we wont save your photo", required=False)
    picture_file = forms.ImageField()
