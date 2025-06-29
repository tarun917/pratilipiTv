# profileDesk/urls.py
from django.urls import path
from .views import ProfileView, ProfileImageUploadView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileView.as_view(), name='profile-update'),
    path('profile/upload-pic/', ProfileImageUploadView.as_view(), name='profile-upload-pic'),
]