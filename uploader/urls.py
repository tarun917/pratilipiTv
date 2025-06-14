from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassicComicViewSet, ModernComicViewSet, SocialDataViewSet, ComicInteractionViewSet

router = DefaultRouter()
router.register(r'comics', ClassicComicViewSet, basename='classic-comic')
router.register(r'motion-comics', ModernComicViewSet, basename='modern-comic')
router.register(r'social-data', SocialDataViewSet, basename='social-data')
router.register(r'interactions', ComicInteractionViewSet, basename='comic-interaction')

urlpatterns = [
    path('', include(router.urls)),
]