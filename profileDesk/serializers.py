# profileDesk/serializers.py
from rest_framework import serializers
from .models import UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    badges = serializers.ListField(child=serializers.CharField(), read_only=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'profile_picture', 'bio', 'badges', 'phone', 'gender', 'date_of_birth']