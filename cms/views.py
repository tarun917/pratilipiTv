# cms/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from communityDesk.models import UserProfile
import logging


logger = logging.getLogger(__name__)
User = get_user_model()

class SignupView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        logger.debug(f"SignupView.post called with data: {request.data}")
        username = request.data.get('username')
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')
        terms_accepted = request.data.get('terms_accepted')

        if not all([username, email, mobile_number, password, terms_accepted]):
            logger.error("Signup failed: Missing required fields")
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not terms_accepted:
            logger.error("Signup failed: Terms not accepted")
            return Response({"error": "You must accept the terms and conditions"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            logger.error(f"Signup failed: Username {username} already exists")
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            logger.error(f"Signup failed: Email {email} already exists")
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(mobile_number=mobile_number).exists():
            logger.error(f"Signup failed: Mobile number {mobile_number} already exists")
            return Response({"error": "Mobile number already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            logger.error(f"Signup failed: Invalid password - {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                full_name=full_name,
                mobile_number=mobile_number,
                password=password,
                terms_accepted=terms_accepted
            )
            # Create UserProfile for the new user
            UserProfile.objects.create(
                user=user,
                bio="",
                phone=mobile_number,
                gender="",
                date_of_birth=None
            )
            refresh = RefreshToken.for_user(user)
            logger.info(f"User created: {username}")
            return Response({
                "token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "userId": user.id,
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Signup failed: {str(e)}")
            return Response({"error": f"Failed to create user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)