from django.db import models
from cms.models import AppUser

class UserProfile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username