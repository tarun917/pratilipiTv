from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

class ClassicComic(models.Model):
    comic_id = models.AutoField(primary_key=True)
    story_title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    image = models.FileField(upload_to='comics/images/', validators=[FileExtensionValidator(['png', 'jpeg'])], blank=False)
    description = models.TextField(blank=True)
    average_rating = models.FloatField(default=0.0)
    view_count = models.IntegerField(default=0)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'classic_comic'

class ClassicEpisode(models.Model):
    episode_id = models.AutoField(primary_key=True)
    comic = models.ForeignKey(ClassicComic, on_delete=models.CASCADE, related_name='episodes')
    episode_title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='comics/pdfs/', validators=[FileExtensionValidator(['pdf'])])
    is_free = models.BooleanField(default=True)
    is_unlocked = models.BooleanField(default=False)

    class Meta:
        db_table = 'classic_episode'

class ModernComic(models.Model):
    motion_comic_id = models.AutoField(primary_key=True)
    story_title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    image = models.FileField(upload_to='comics/images/', validators=[FileExtensionValidator(['png', 'jpeg'])], blank=False)
    description = models.TextField(blank=True)
    average_rating = models.FloatField(default=0.0)
    view_count = models.IntegerField(default=0)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'modern_comic'

class ModernEpisode(models.Model):
    episode_id = models.AutoField(primary_key=True)
    comic = models.ForeignKey(ModernComic, on_delete=models.CASCADE, related_name='episodes')
    episode_title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='comics/videos/', validators=[FileExtensionValidator(['mp4'])])
    is_free = models.BooleanField(default=False)
    is_unlocked = models.BooleanField(default=True)

    class Meta:
        db_table = 'modern_episode'

class ComicPage(models.Model):
    id = models.AutoField(primary_key=True)
    classic_episode = models.ForeignKey(ClassicEpisode, on_delete=models.CASCADE, null=True, blank=True, related_name='pages')
    modern_episode = models.ForeignKey(ModernEpisode, on_delete=models.CASCADE, null=True, blank=True, related_name='pages')
    image_url = models.URLField(max_length=500)
    text = models.TextField()

    class Meta:
        db_table = 'comic_page'

class SocialData(models.Model):
    id = models.AutoField(primary_key=True)
    classic_comic = models.ForeignKey(ClassicComic, on_delete=models.CASCADE, null=True, blank=True)
    modern_comic = models.ForeignKey(ModernComic, on_delete=models.CASCADE, null=True, blank=True)
    classic_episode = models.ForeignKey(ClassicEpisode, on_delete=models.CASCADE, null=True, blank=True)
    modern_episode = models.ForeignKey(ModernEpisode, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('cms.AppUser', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    tags = models.JSONField(default=list)
    comments = models.JSONField(default=list)

    class Meta:
        db_table = 'social_data'

class ComicInteraction(models.Model):
    id = models.AutoField(primary_key=True)
    classic_comic = models.ForeignKey(ClassicComic, on_delete=models.CASCADE, null=True, blank=True)
    modern_comic = models.ForeignKey(ModernComic, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('cms.AppUser', on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comic_interaction'
        constraints = [
            models.UniqueConstraint(
                fields=['classic_comic', 'user'],
                condition=models.Q(modern_comic__isnull=True),
                name='unique_classic_comic_user'
            ),
            models.UniqueConstraint(
                fields=['modern_comic', 'user'],
                condition=models.Q(classic_comic__isnull=True),
                name='unique_modern_comic_user'
            ),
            models.CheckConstraint(
                check=~models.Q(classic_comic__isnull=True, modern_comic__isnull=True) & ~models.Q(classic_comic__isnull=False, modern_comic__isnull=False),
                name='one_comic_only'
            )
        ]