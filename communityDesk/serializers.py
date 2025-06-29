# communityDesk/serializers.py
from rest_framework import serializers
from django.db.models import Count
from django.conf import settings
from .models import UserProfile, CommunityPost, Comment, Poll, PollOption, PollVote, Reaction, Follow
from cms.models import AppUser
import logging

logger = logging.getLogger(__name__)

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'profile_picture', 'bio', 'badges', 'phone', 'gender', 'date_of_birth']

    def to_representation(self, instance):
        if instance is None:
            return {
                "username": "string",
                "email": "string",
                "profile_picture": "string|null",
                "bio": "string",
                "badges": ["string"],
                "phone": "string",
                "gender": "string",
                "date_of_birth": "string|null"
            }
        representation = super().to_representation(instance)
        representation['badges'] = [badge['name'] for badge in instance.badges] if instance.badges else []
        return representation

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'profile_picture', 'bio', 'badges', 'phone', 'gender', 'date_of_birth']
        read_only_fields = ['username', 'email', 'badges']

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.badges = validated_data.get('badges', instance.badges)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance

class UserSearchSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    phone = serializers.CharField(source='community_profile.phone', read_only=True, allow_null=True)
    gender = serializers.CharField(source='community_profile.gender', read_only=True, allow_null=True)
    date_of_birth = serializers.DateField(source='community_profile.date_of_birth', read_only=True, allow_null=True)

    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email', 'profile_picture', 'phone', 'gender', 'date_of_birth']

    def get_profile_picture(self, obj):
        logger.debug(f"UserSearchSerializer.get_profile_picture called for obj: {obj}")
        try:
            profile = obj.community_profile
            logger.debug(f"Profile found for user {obj.username}: {profile}")
            return profile.profile_picture.url if profile.profile_picture else None
        except UserProfile.DoesNotExist:
            logger.debug(f"No UserProfile found for user {obj.username}")
            return None
        except Exception as e:
            logger.error(f"Error in get_profile_picture for user {obj.username}: {str(e)}")
            raise

class PollOptionSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = PollOption
        fields = ['id', 'text', 'vote_count']

class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True)
    voted_option = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', 'question', 'options', 'voted_option', 'created_at']

    def get_voted_option(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = PollVote.objects.filter(user=request.user, option__poll=obj).first()
            return vote.option.id if vote else None
        return None

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True, source='user.community_profile')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class CommunityPostSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True, source='user.community_profile')
    poll = PollSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    reactions = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = CommunityPost
        fields = [
            'id', 'user', 'content', 'image', 'poll', 'comments', 'reactions',
            'is_commenting_enabled', 'created_at', 'updated_at', 'is_following'
        ]

    def get_reactions(self, obj):
        reactions = obj.reactions.values('reaction_type').annotate(count=Count('reaction_type'))
        user_reaction = obj.reactions.filter(user=self.context['request'].user).first()
        return {
            'heart': {
                'count': next((r['count'] for r in reactions if r['reaction_type'] == 'heart'), 0),
                'has_reacted': user_reaction.reaction_type == 'heart' if user_reaction else False
            }
        }

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(follower=request.user, followed=obj.user).exists()
        return False

class ReactionSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True, source='user.community_profile')

    class Meta:
        model = Reaction
        fields = ['id', 'user', 'post', 'reaction_type', 'created_at']

    def validate_reaction_type(self, value):
        if value not in ['heart']:
            raise serializers.ValidationError("Invalid reaction type")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        post = validated_data['post']
        reaction_type = validated_data['reaction_type']
        reaction = Reaction.objects.filter(user=request.user, post=post, reaction_type=reaction_type)
        if reaction.exists():
            reaction.delete()
            return None
        return Reaction.objects.create(user=request.user, reaction_type=reaction_type, post=post)

class PollVoteSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True, source='user.community_profile')
    option = PollOptionSerializer(read_only=True)

    class Meta:
        model = PollVote
        fields = ['id', 'user', 'option', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to vote")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        option = validated_data['option']
        PollVote.objects.filter(user=request.user, option__poll=option.poll).delete()
        option.vote_count += 1
        option.save()
        return PollVote.objects.create(user=request.user, option=option)

class FollowSerializer(serializers.ModelSerializer):
    follower = UserProfileSerializer(read_only=True, source='follower.community_profile')
    followed = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all(), required=False)
    followed_username = serializers.CharField(write_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'followed_username', 'created_at']

    def validate(self, attrs):
        logger.debug(f"FollowSerializer.validate called with attrs: {attrs}")
        request = self.context.get('request')
        if not request.user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to follow")
        followed_username = attrs.get('followed_username')
        try:
            followed = AppUser.objects.get(username=followed_username)
            if followed == request.user:
                raise serializers.ValidationError("You cannot follow yourself")
            attrs['followed'] = followed
            UserProfile.objects.get_or_create(user=followed)
        except AppUser.DoesNotExist:
            logger.error(f"Follow failed: User {followed_username} not found")
            raise serializers.ValidationError("User not found")
        except Exception as e:
            logger.error(f"Failed to ensure UserProfile for followed user: {str(e)}")
            raise serializers.ValidationError(f"Failed to process follow: {str(e)}")
        return attrs

    def create(self, validated_data):
        logger.debug(f"FollowSerializer.create called with validated_data: {validated_data}")
        request = self.context.get('request')
        followed = validated_data['followed']
        try:
            follow, created = Follow.objects.get_or_create(follower=request.user, followed=followed)
            logger.info(f"Follow created: {request.user.username} -> {followed.username}")
            return follow
        except Exception as e:
            logger.error(f"Failed to create follow: {str(e)}")
            raise serializers.ValidationError(f"Failed to create follow: {str(e)}")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['followed'] = UserProfileSerializer(instance.followed.community_profile).data
        return representation