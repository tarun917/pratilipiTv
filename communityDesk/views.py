from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.conf import settings
from .models import CommunityPost, Comment, Poll, PollOption, PollVote, Reaction, Follow, UserProfile
from cms.models import AppUser
from .serializers import (
    CommunityPostSerializer, CommentSerializer, PollSerializer, PollVoteSerializer,
    UserSearchSerializer, FollowSerializer, ReactionSerializer
)
import logging

logger = logging.getLogger(__name__)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class CommunityPostViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all().order_by('-created_at')
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        poll_data = self.request.data.get('poll')
        content = self.request.data.get('content', '')
        words = len(content.strip().split()) if content else 0
        if words > 512:
            raise serializers.ValidationError("Content exceeds 512 words")
        post = serializer.save(user=self.request.user)
        if poll_data:
            options = poll_data.get('options', [])
            if len(options) < 2:
                raise serializers.ValidationError("Poll must have at least 2 options")
            if len(options) > 6:
                raise serializers.ValidationError("Poll cannot have more than 6 options")
            poll = Poll.objects.create(post=post, question=poll_data.get('question', ''))
            for option_text in options:
                PollOption.objects.create(poll=poll, text=option_text)
        UserProfile.objects.get_or_create(user=self.request.user)

    def perform_update(self, serializer):
        poll_data = self.request.data.get('poll')
        content = self.request.data.get('content', '')
        words = len(content.strip().split()) if content else 0
        if words > 512:
            raise serializers.ValidationError("Content exceeds 512 words")
        post = serializer.save()
        if poll_data and post.poll:
            post.poll.question = poll_data.get('question', post.poll.question)
            post.poll.save()
            PollOption.objects.filter(poll=post.poll).delete()
            options = poll_data.get('options', [])
            if len(options) < 2:
                raise serializers.ValidationError("Poll must have at least 2 options")
            if len(options) > 6:
                raise serializers.ValidationError("Poll cannot have more than 6 options")
            for option_text in options:
                PollOption.objects.create(poll=post.poll, text=option_text)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def toggle_commenting(self, request, pk=None):
        post = self.get_object()
        if post.user != request.user:
            return Response({"error": "Only the post owner can toggle commenting"}, status=status.HTTP_403_FORBIDDEN)
        post.is_commenting_enabled = not post.is_commenting_enabled
        post.save()
        return Response({"is_commenting_enabled": post.is_commenting_enabled}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'get', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def reactions(self, request, pk=None):
        post = self.get_object()
        try:
            UserProfile.objects.get_or_create(user=request.user)
            reaction_type = request.data.get('reaction_type', request.query_params.get('reaction_type', 'heart'))
            if reaction_type not in ['heart']:
                return Response({"error": "Invalid reaction type"}, status=status.HTTP_400_BAD_REQUEST)
            if request.method == 'POST':
                try:
                    serializer = ReactionSerializer(data={'post': post.id, 'reaction_type': reaction_type}, context={'request': request})
                    serializer.is_valid(raise_exception=True)
                    reaction = serializer.create(serializer.validated_data)
                    if reaction is None:
                        return Response({"message": "Reaction removed"}, status=status.HTTP_200_OK)
                    return Response({"message": "Reaction added"}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    logger.error(f"Failed to process reaction for post {pk}: {str(e)}")
                    return Response({"error": f"Failed to process reaction: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif request.method == 'GET':
                reactions = post.reactions.filter(reaction_type=reaction_type).values('reaction_type').annotate(count=Count('reaction_type'))
                user_reaction = post.reactions.filter(user=request.user, reaction_type=reaction_type).exists()
                return Response({
                    reaction_type: {
                        'count': next((r['count'] for r in reactions if r['reaction_type'] == reaction_type), 0),
                        'has_reacted': user_reaction
                    }
                }, status=status.HTTP_200_OK)
            elif request.method == 'DELETE':
                reaction = post.reactions.filter(user=request.user, reaction_type=reaction_type)
                if reaction.exists():
                    reaction.delete()
                    return Response({"message": "Reaction removed"}, status=status.HTTP_200_OK)
                return Response({"error": "Reaction not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Server error in reactions for post {pk}: {str(e)}")
            return Response({"error": f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('created_at')

    def perform_create(self, serializer):
        post = CommunityPost.objects.get(id=self.kwargs['post_id'])
        if not post.is_commenting_enabled:
            raise serializers.ValidationError("Commenting is disabled for this post")
        serializer.save(user=self.request.user, post=post)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.user != self.request.user:
            raise serializers.ValidationError("You can only edit your own comments")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise serializers.ValidationError("You can only delete your own comments")
        instance.delete()

class PollVoteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, post_id=None):
        poll = Poll.objects.filter(post_id=post_id).first()
        if not poll:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PollSerializer(poll, context={'request': request})
        return Response(serializer.data)

    def create(self, request, post_id=None):
        logger.debug(f"PollVoteViewSet.create called for post_id: {post_id}, data: {request.data}")
        option_id = request.data.get('option_id')
        try:
            option = PollOption.objects.get(id=option_id, poll__post_id=post_id)
        except PollOption.DoesNotExist:
            logger.error(f"Invalid poll option: {option_id} for post_id: {post_id}")
            return Response({"error": "Invalid poll option"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = PollVoteSerializer(data={'option': option}, context={'request': request})
            if serializer.is_valid():
                serializer.create({'option': option})
                logger.info(f"Vote recorded for user: {request.user.username}, option_id: {option_id}")
                return Response({"message": "Vote recorded"}, status=status.HTTP_201_CREATED)
            logger.error(f"Poll vote validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Failed to process poll vote for option_id {option_id}: {str(e)}")
            return Response({"error": f"Failed to process vote: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, post_id=None, pk=None):
        poll = Poll.objects.filter(post_id=post_id, id=pk).first()
        if not poll:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PollSerializer(poll, context={'request': request})
        return Response(serializer.data)

    def update(self, request, post_id=None, pk=None):
        return Response({"error": "Updating polls is not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, post_id=None, pk=None):
        return Response({"error": "Deleting polls is not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserSearchViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        logger.debug(f"UserSearchViewSet.list called with query: {request.query_params.get('q', '')}")
        try:
            query = request.query_params.get('q', '')
            users = AppUser.objects.filter(
                Q(username__icontains=query) | Q(community_profile__bio__icontains=query)
            ).exclude(id=request.user.id)[:10]
            serializer = UserSearchSerializer(users, many=True, context={'request': request})
            logger.info(f"User search returned {len(users)} results for query: {query}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"User search failed: {str(e)}")
            return Response({"error": f"Failed to process search: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        logger.debug(f"FollowViewSet.perform_create called with data: {self.request.data}")
        try:
            serializer.is_valid(raise_exception=True)
            follow = serializer.save(follower=self.request.user)
            logger.info(f"Follow created: {self.request.user.username} -> {self.request.data.get('followed_username')}")
            return Response(FollowSerializer(follow, context={'request': self.request}).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Follow failed: {str(e)}")
            raise serializers.ValidationError(f"Failed to process follow: {str(e)}")