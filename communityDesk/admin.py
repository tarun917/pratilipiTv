from django.contrib import admin
from .models import CommunityPost, UserProfile, Comment, Poll, PollOption, PollVote, Reaction, Follow

# Register models
admin.site.register(CommunityPost)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(PollVote)
admin.site.register(Reaction)
admin.site.register(Follow)