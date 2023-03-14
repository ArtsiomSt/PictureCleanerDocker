from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"class": "form-control"}), label='Password')


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"class": "form-control"}), label='Password')
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"class": "form-control"}), label='Repeat password')


class ChangeUserProfileDataForm(forms.Form):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)


class SetNewPassword(SetPasswordForm):
    pass


class AddPictureForRecogintionForm(forms.Form):
    save_or_not = forms.BooleanField(label="Press here and we will delete your photo after sign out", required=False)
    picture_file = forms.ImageField()
