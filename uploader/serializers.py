from rest_framework import serializers
from .models import ClassicComic, ClassicEpisode, ModernComic, ModernEpisode, ComicPage, SocialData, ComicInteraction
from cms.models import AppUser

class ComicPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicPage
        fields = ['id', 'image_url', 'text']

class ClassicEpisodeSerializer(serializers.ModelSerializer):
    pages = ComicPageSerializer(many=True, read_only=True)

    class Meta:
        model = ClassicEpisode
        fields = ['episode_id', 'episode_title', 'pdf_file', 'is_free', 'is_unlocked', 'pages']

class ModernEpisodeSerializer(serializers.ModelSerializer):
    pages = ComicPageSerializer(many=True, read_only=True)

    class Meta:
        model = ModernEpisode
        fields = ['episode_id', 'episode_title', 'video_file', 'is_free', 'is_unlocked', 'pages']

class ClassicComicSerializer(serializers.ModelSerializer):
    episodes = ClassicEpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = ClassicComic
        fields = ['comic_id', 'story_title', 'genre', 'image', 'description', 'average_rating', 'view_count', 'episodes']

class ModernComicSerializer(serializers.ModelSerializer):
    episodes = ModernEpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = ModernComic
        fields = ['motion_comic_id', 'story_title', 'genre', 'image', 'description', 'average_rating', 'view_count', 'episodes']

class SocialDataSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())

    class Meta:
        model = SocialData
        fields = ['id', 'classic_comic', 'modern_comic', 'classic_episode', 'modern_episode', 'user', 'is_liked', 'like_count', 'tags', 'comments']

class ComicInteractionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = ComicInteraction
        fields = ['id', 'classic_comic', 'modern_comic', 'user', 'rating', 'viewed', 'created_at']

    def validate(self, data):
        if data.get('classic_comic') and data.get('modern_comic'):
            raise serializers.ValidationError("Only one of classic_comic or modern_comic can be set.")
        if not data.get('classic_comic') and not data.get('modern_comic'):
            raise serializers.ValidationError("One of classic_comic or modern_comic must be set.")
        return data