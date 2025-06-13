from django.db import models

class AppUser(models.Model):
    """
    Model to store Android app signup users for PratilipiTv.
    Contains credentials for signup process.
    """
    full_name = models.CharField(
        max_length=255,
        help_text="User's full name.",
    )
    email = models.EmailField(
        unique=True,
        help_text="User's email address.",
    )
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        help_text="User's mobile number (e.g., +919876543210).",
    )
    password = models.CharField(
        max_length=128,
        help_text="Hashed user password.",
    )
    terms_accepted = models.BooleanField(
        default=False,
        help_text="Indicates if user agreed to terms and conditions.",
    )

    class Meta:
        db_table = "app_user"
        verbose_name = "App User"
        verbose_name_plural = "App Users"

    def __str__(self):
        return self.email