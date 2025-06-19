from rest_framework import serializers
from .models import AppUser
import re
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

class AppUserSerializer(serializers.ModelSerializer):
    """
    Serializer for AppUser model to handle Android app signup data.
    Validates full_name, email, mobile_number, password, username, and terms_accepted.
    """
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = AppUser
        fields = ['username', 'full_name', 'email', 'mobile_number', 'password', 'terms_accepted']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_username(self, value):
        """Ensure username is unique and valid."""
        if not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        if AppUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if not re.match(r'^[A-Za-z0-9_.-]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers, underscores, dots, or hyphens.")
        return value

    def validate_full_name(self, value):
        """Ensure full_name is not empty and contains only letters, spaces, or hyphens."""
        if not value.strip():
            raise serializers.ValidationError("Full name cannot be empty.")
        if not re.match(r'^[A-Za-z\s-]+$', value):
            raise serializers.ValidationError("Full name can only contain letters, spaces, or hyphens.")
        return value

    def validate_email(self, value):
        """Ensure email is unique and valid."""
        if AppUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value.lower()

    def validate_mobile_number(self, value):
        """Ensure mobile_number is valid and unique."""
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise serializers.ValidationError("Invalid mobile number format (e.g., +919876543210).")
        if AppUser.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("This mobile number is already registered.")
        return value

    def validate_terms_accepted(self, value):
        """Ensure terms_accepted is True."""
        if not value:
            raise serializers.ValidationError("You must agree to the terms and conditions.")
        return value

    def validate_password(self, value):
        """Ensure password meets minimum length requirement."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        """Create a new AppUser with hashed password."""
        user = AppUser(
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            terms_accepted=validated_data['terms_accepted'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for login requests.
    Validates username or email and password, returns JWT tokens.
    """
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """Validate username/email and password."""
        username_or_email = data.get('username_or_email').lower()
        password = data.get('password')

        # Try authenticating with username or email
        user = None
        if '@' in username_or_email:
            try:
                user = AppUser.objects.get(email=username_or_email)
            except AppUser.DoesNotExist:
                pass
        else:
            try:
                user = AppUser.objects.get(username=username_or_email)
            except AppUser.DoesNotExist:
                pass

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid username/email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'userId': user.id,
            'username': user.username
        }