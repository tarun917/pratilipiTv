# communityDesk/management/commands/create_user_profiles.py
from django.core.management.base import BaseCommand
from cms.models import AppUser
from communityDesk.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile for existing AppUser instances'

    def handle(self, *args, **options):
        for user in AppUser.objects.all():
            UserProfile.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}'))