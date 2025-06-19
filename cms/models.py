from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    """
    Model to store Android app signup users for PratilipiTv.
    Extends AbstractUser for Django authentication compatibility.
    """
    full_name = models.CharField(
        max_length=255,
        help_text="User's full name.",
    )
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        help_text="User's mobile number (e.g., +919876543210).",
    )
    terms_accepted = models.BooleanField(
        default=False,
        help_text="Indicates if user agreed to terms and conditions.",
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='appuser_groups',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='appuser_permissions',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    class Meta:
        db_table = "app_user"
        verbose_name = "App User"
        verbose_name_plural = "App Users"

    def __str__(self):
        return self.email