# communityDesk/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from cms.models import AppUser
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='community_profile'
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    badges = models.JSONField(default=list)
    phone = models.CharField(max_length=15, blank=True)  # From profileDesk
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")], blank=True)  # From profileDesk
    date_of_birth = models.DateField(null=True, blank=True)  # From profileDesk

    def __str__(self):
        return self.user.username

class CommunityPost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(max_length=512 * 5)  # ~5 chars/word
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_commenting_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Post {self.id} by {self.user.username}"

class Comment(models.Model):
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"

class Poll(models.Model):
    post = models.OneToOneField(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name='poll'
    )
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Poll for Post {self.post.id}"

class PollOption(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='options'
    )
    text = models.CharField(max_length=100)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Option: {self.text} for Poll {self.poll.id}"

class PollVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='poll_votes'
    )
    option = models.ForeignKey(
        PollOption,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'option')

    def __str__(self):
        return f"Vote by {self.user.username} for {self.option.text}"

class Reaction(models.Model):
    REACTION_TYPES = (
        ('heart', 'Heart'),
    )
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user', 'reaction_type')

    def __str__(self):
        return f"{self.reaction_type} by {self.user.username} on Post {self.post.id}"

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"