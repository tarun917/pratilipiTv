# communityDesk/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommunityPostViewSet, CommentViewSet, PollVoteViewSet, UserSearchViewSet, FollowViewSet
)

router = DefaultRouter()
router.register(r'posts', CommunityPostViewSet, basename='post')
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'polls', PollVoteViewSet, basename='poll')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='post-comment-detail'),
    path('posts/<int:post_id>/polls/', PollVoteViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-polls'),
    path('posts/<int:post_id>/polls/<int:poll_id>/', PollVoteViewSet.as_view({'get': 'retrieve'}), name='post-poll-detail'),
    path('posts/<int:post_id>/poll_votes/', PollVoteViewSet.as_view({'post': 'create'}), name='post-poll-votes'),
    path('posts/<int:post_id>/reactions/', CommunityPostViewSet.as_view({'post': 'reactions', 'get': 'reactions', 'delete': 'reactions'}), name='post-reactions'),
    path('posts/<int:post_id>/toggle_commenting/', CommunityPostViewSet.as_view({'patch': 'toggle_commenting'}), name='toggle-commenting'),
    path('users/search/', UserSearchViewSet.as_view({'get': 'list'}), name='user-search-list'),
]