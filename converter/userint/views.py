import os
import mimetypes
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .mixins import LoginRequiredRedirectMixin
from .forms import LoginForm, RegisterForm, ChangeUserProfileDataForm, SetNewPassword, AddPictureForRecogintionForm
from .models import UserProfile, PictureForRecongition
import requests
from converter.settings import BASE_DIR, MEDIA_ROOT
import base64
import cv2
import io


class HomePageView(LoginRequiredRedirectMixin, View):
    def get(self, request):
        form = AddPictureForRecogintionForm()
        context = {
            'form': form,
            'title': 'Homepage',
        }
        return render(request, 'userint/homepage.html', context=context)

    def post(self, request):
        form = AddPictureForRecogintionForm(request.POST, request.FILES)
        if form.is_valid():
            current_picture = PictureForRecongition.objects.create(
                made_by_user=UserProfile.objects.get(user=request.user),
                picture_file=form.cleaned_data['picture_file'])

            media = current_picture.picture_file.url[1:]
            url = "http://0.0.0.0:4000/recpicture/api/v1/recognise/"
            payload = {}
            files = [('image', ('recognise.png', open(media, 'rb'), 'image/png'))]
            headers = {}
            resp = requests.request("POST", url, headers=headers, data=payload, files=files)

            image_code = resp.json().get('new_img', None)
            cleaned_image_opencv = resp.json().get('cleaned_img', None)
            text_from_picture = resp.json().get('letters', None)
            autoencoded_image = resp.json().get('autoencoded_img', None)

            if image_code is not None:
                image_decode = base64.b64decode(image_code)
                buffer = io.BytesIO()
                buffer.write(image_decode)
                buffer.seek(0)
                rectangled_image_file = File(buffer, 'image.png')
                current_picture.rectangled_image = rectangled_image_file

            if text_from_picture is not None:
                current_picture.recognised_text = text_from_picture

            if cleaned_image_opencv is not None:
                cleaned_image_decode = base64.b64decode(cleaned_image_opencv)
                buffer = io.BytesIO()
                buffer.write(cleaned_image_decode)
                buffer.seek(0)
                cleaned_image_file = File(buffer, 'image.png')
                current_picture.cleaned_opencv_image = cleaned_image_file

            if autoencoded_image is not None:
                autoencoded_image_decode = base64.b64decode(autoencoded_image)
                buffer = io.BytesIO()
                buffer.write(autoencoded_image_decode)
                buffer.seek(0)
                autoencoded_image_file = File(buffer, 'image.png')
                current_picture.autoencoded_image = autoencoded_image_file

            current_picture.save()
            context = {
                'title': 'Homepage',
                'current_picture': current_picture,
                'opencvimage_code': f'{current_picture.pk}_img_co',
                'autoencoded_code': f'{current_picture.pk}_img_ca',
            }
            return render(request, 'userint/homepage.html', context=context)
        return redirect('/?Error')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'userint/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            try:
                login(request, user)
                return redirect('home')
            except:
                pass
        return redirect('/signin/?message=InvalidData')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'userint/registration.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('/signin/?message=Success')
        return redirect('/signup/?message=Invaliddata')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')


class ProfileView(LoginRequiredRedirectMixin, View):
    def get(self, request):
        import random
        cur_user = UserProfile.objects.select_related().get(user=request.user)
        form = SetNewPassword(cur_user.user)
        user_data = {
            'Username': cur_user.user.username,
            'First name': cur_user.user.first_name if cur_user.user.first_name else 'Empty',
            'Last name': cur_user.user.last_name if cur_user.user.first_name else 'Empty',
            'Email': cur_user.user.email if cur_user.user.first_name else 'Empty',
            'Password': ''.join(['*' for x in range(0, random.randrange(5, 10))])
        }
        context = {
            'user_data': user_data,
            'title': 'Profile',
        }
        if request.GET.get('chps') == 'true':
            context['form'] = form
        return render(request, 'userint/profile.html', context)

    def post(self, request):
        cur_user = UserProfile.objects.select_related().get(user=request.user)
        form = SetNewPassword(user=cur_user.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return redirect('profile')


class ChangeProfileDataView(LoginRequiredRedirectMixin, View):
    def get(self, request):
        cur_user = UserProfile.objects.select_related().get(user=request.user)
        user_data = {
            'username': cur_user.user.username,
            'first_name': cur_user.user.first_name if cur_user.user.first_name else 'Empty',
            'last_name': cur_user.user.last_name if cur_user.user.first_name else 'Empty',
            'email': cur_user.user.email if cur_user.user.first_name else 'Empty',
        }
        user_data_change_form = ChangeUserProfileDataForm(initial=user_data)
        context = {
            'change_form': user_data_change_form,
            'title': 'ChangeProfile',
        }
        return render(request, 'userint/changeprofile.html', context)

    def post(self, request):
        cur_user = UserProfile.objects.select_related().get(user=request.user)
        user_data_change_form = ChangeUserProfileDataForm(request.POST)
        if user_data_change_form.is_valid():
            cur_user.user.first_name = user_data_change_form.cleaned_data.get('first_name')
            cur_user.user.last_name = user_data_change_form.cleaned_data.get('last_name')
            cur_user.user.email = user_data_change_form.cleaned_data.get('email')
            cur_user.user.username = user_data_change_form.cleaned_data.get('username')
            cur_user.user.save()
            cur_user.save()
        return redirect('profile')


def download_pdf(request):
    filename = 'img.png'
    filepath = os.path.join(MEDIA_ROOT, filename)
    with open(filepath, 'rb') as path:
        try:
            mime_type, _ = mimetypes.guess_type(filepath)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
        except:
            return HttpResponse('Error while downloading file')
    return response


def download_file(request, filecode):  # filecode = str, where first value is id of image and the second value is file type
    file_stats = filecode.split('_')
    if len(file_stats) not in [2,3]:
        print('1')
        return redirect('home')
    print(file_stats)
    if not (file_stats[0].isdigit() and file_stats[1] in ['img']):
        print('2')
        return redirect('home')
    user = UserProfile.objects.get(user=request.user)
    image_for_download = user.pictureforrecongition_set.get(pk=int(file_stats[0]))
    if file_stats[1] == 'img':
        filename = 'img.png'
        if file_stats[2] == 'co':
            filepath = image_for_download.cleaned_opencv_image.url[1:]
        elif file_stats[2] == 'ca':
            filepath = image_for_download.autoencoded_image.url[1:]
        else:
            print('3')
            return redirect('home')
    print(filepath)
    with open(filepath, 'rb') as path:
        try:
            mime_type, _ = mimetypes.guess_type(filepath)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
        except:
            return HttpResponse('Error while downloading file')
    return response
