# profileDesk/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from communityDesk.models import UserProfile
from communityDesk.serializers import UserProfileSerializer, UserProfileUpdateSerializer
import logging

logger = logging.getLogger(__name__)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.debug(f"ProfileView.get called for user: {request.user.username}")
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            logger.info(f"Profile found for user: {request.user.username}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile not found for user: {request.user.username}")
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        logger.debug(f"ProfileView.put called for user: {request.user.username}, data: {request.data}")
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Profile updated for user: {request.user.username}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(f"Profile update failed for user: {request.user.username}, errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile not found for user: {request.user.username}")
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

class ProfileImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        logger.debug(f"ProfileImageUploadView.post called for user: {request.user.username}, data: {request.data}")
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Profile image updated for user: {request.user.username}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(f"Profile image update failed for user: {request.user.username}, errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile not found for user: {request.user.username}")
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)