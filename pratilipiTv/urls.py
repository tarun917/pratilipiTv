# pratilipiTv/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from cms.views import SignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/cms/', include('cms.urls')),
    path('api/communityDesk/', include('communityDesk.urls')),
    path('api/profileDesk/', include('profileDesk.urls')),
    path('api/uploader/', include('uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)