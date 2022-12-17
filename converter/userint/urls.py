from django.urls import path
from .views import *
from converter.settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('logout/', logout_user, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('changeprofile/', ChangeProfileDataView.as_view(), name='changep'),
    path('dowload/imgtest/', download_pdf, name='dtest'),
    path('download/<str:filecode>', download_file, name='download'),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
