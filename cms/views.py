from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import AppUserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(generics.CreateAPIView):
    """
    API view to handle user signup for PratilipiTv Android app.
    Accepts POST requests with full_name, email, mobile_number, password, and terms_accepted.
    """
    serializer_class = AppUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "userId": user.id,
                    "username": user.full_name
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    """
    API view to handle user login for PratilipiTv Android app.
    Accepts POST requests with email and password, returns JWT tokens.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)