from django.db.models.signals import post_save
from django.dispatch import receiver
from cms.models import AppUser
from .models import UserProfile

@receiver(post_save, sender=AppUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)