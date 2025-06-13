from django.contrib import admin
from .models import AppUser

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    """
    Admin configuration for AppUser model.
    Displays and manages Android app signup users under PRATILIPI_TV category.
    """
    list_display = ["email", "full_name", "mobile_number", "terms_accepted"]
    search_fields = ["email", "full_name", "mobile_number"]
    list_filter = ["terms_accepted"]
    readonly_fields = ["password"]  # Password is read-only in admin
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("full_name", "email", "mobile_number", "password", "terms_accepted"),
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset for performance."""
        return super().get_queryset(request).select_related()

    def get_app_label(self):
        """Customize the app name displayed in admin."""
        return "PRATILIPI_TV"

    def get_form(self, request, obj=None, **kwargs):
        """Ensure required fields in the form, excluding password."""
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["email"].required = True
        form.base_fields["full_name"].required = True
        form.base_fields["mobile_number"].required = True
        # Password is not required in admin form (handled by API)
        return form