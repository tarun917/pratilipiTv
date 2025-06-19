from django.contrib import admin
from .models import ClassicComic, ModernComic, ClassicEpisode, ModernEpisode, ComicPage, SocialData, ComicInteraction
from cms.models import AppUser

class ComicPageInline(admin.TabularInline):
    model = ComicPage
    extra = 1
    fields = ('image_url', 'text')

class ClassicEpisodeInline(admin.TabularInline):
    model = ClassicEpisode
    extra = 1
    fields = ('episode_title', 'pdf_file', 'is_free', 'is_unlocked')
    min_num = 1
    inlines = [ComicPageInline]

class ModernEpisodeInline(admin.TabularInline):
    model = ModernEpisode
    extra = 1
    fields = ('episode_title', 'video_file', 'is_free', 'is_unlocked')
    min_num = 1
    inlines = [ComicPageInline]

class ClassicComicAdmin(admin.ModelAdmin):
    list_display = ('story_title', 'genre', 'average_rating', 'view_count')
    list_filter = ('genre',)
    search_fields = ('story_title',)
    inlines = [ClassicEpisodeInline]
    fieldsets = (
        (None, {
            'fields': ('story_title', 'genre', 'image', 'description', 'uploader')
        }),
    )
    readonly_fields = ('uploader', 'average_rating', 'view_count')

    def save_model(self, request, obj, form, change):
        # Map auth.User to cms.AppUser
        try:
            app_user = AppUser.objects.get(email=request.user.email)
        except AppUser.DoesNotExist:
            # Create a new AppUser if none exists
            app_user = AppUser.objects.create(
                username=request.user.username,
                email=request.user.email,
                full_name=f"{request.user.first_name} {request.user.last_name}".strip(),
                mobile_number='+919999999999',  # Default placeholder, adjust as needed
                terms_accepted=True,
                is_staff=request.user.is_staff,
                is_superuser=request.user.is_superuser
            )
            app_user.set_password('default_password')  # Set a default password
            app_user.save()
        obj.uploader = app_user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['image'].required = True
        return form

class ModernComicAdmin(admin.ModelAdmin):
    list_display = ('story_title', 'genre', 'average_rating', 'view_count')
    list_filter = ('genre',)
    search_fields = ('story_title',)
    inlines = [ModernEpisodeInline]
    fieldsets = (
        (None, {
            'fields': ('story_title', 'genre', 'image', 'description', 'uploader')
        }),
    )
    readonly_fields = ('uploader', 'average_rating', 'view_count')

    def save_model(self, request, obj, form, change):
        # Map auth.User to cms.AppUser
        try:
            app_user = AppUser.objects.get(email=request.user.email)
        except AppUser.DoesNotExist:
            # Create a new AppUser if none exists
            app_user = AppUser.objects.create(
                username=request.user.username,
                email=request.user.email,
                full_name=f"{request.user.first_name} {request.user.last_name}".strip(),
                mobile_number='+919999999999',  # Default placeholder, adjust as needed
                terms_accepted=True,
                is_staff=request.user.is_staff,
                is_superuser=request.user.is_superuser
            )
            app_user.set_password('default_password')  # Set a default password
            app_user.save()
        obj.uploader = app_user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['image'].required = True
        return form

admin.site.register(ClassicComic, ClassicComicAdmin)
admin.site.register(ModernComic, ModernComicAdmin)
admin.site.register(SocialData)
admin.site.register(ComicInteraction)