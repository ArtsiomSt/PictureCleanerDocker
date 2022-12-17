from django.urls import path
from .views import *


urlpatterns = [
    path('api/v1/recognise/', RecognisePictureAPIView.as_view(), name='recognise'),
]