from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ClassicComic, ModernComic, SocialData, ComicInteraction
from .serializers import ClassicComicSerializer, ModernComicSerializer, SocialDataSerializer, ComicInteractionSerializer
from .permissions import IsAdminOrReadOnly

class ClassicComicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClassicComic.objects.all()
    serializer_class = ClassicComicSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)
        return queryset

class ModernComicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModernComic.objects.all()
    serializer_class = ModernComicSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)
        return queryset

class SocialDataViewSet(viewsets.ModelViewSet):
    queryset = SocialData.objects.all()
    serializer_class = SocialDataSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        comic_id = self.request.query_params.get('comic_id')
        episode_id = self.request.query_params.get('episode_id')
        if comic_id:
            queryset = queryset.filter(classic_comic_id=comic_id) | queryset.filter(modern_comic_id=comic_id)
        if episode_id:
            queryset = queryset.filter(classic_episode_id=episode_id) | queryset.filter(modern_episode_id=episode_id)
        return queryset

class ComicInteractionViewSet(viewsets.ModelViewSet):
    queryset = ComicInteraction.objects.all()
    serializer_class = ComicInteractionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_staff:
            queryset = queryset.filter(user__email=user.email)
        comic_id = self.request.query_params.get('comic_id')
        if comic_id:
            queryset = queryset.filter(classic_comic_id=comic_id) | queryset.filter(modern_comic_id=comic_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)