from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
)


class RegisterView(APIView):
    """
    Handle user registration.
    POST /api/auth/register/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Create user
            user = serializer.save()

            # Generate auth token for new user
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "status": "success",
                    "message": "Account created successfully.",
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "full_name": user.get_full_name(),
                        "date_joined": user.date_joined,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "status": "error",
                "message": "Registration failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    Handle user login.
    POST /api/auth/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Login user (creates session)
            login(request, user)

            # Get or create auth token
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "status": "success",
                    "message": "Login successful.",
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "full_name": user.get_full_name(),
                        "date_joined": user.date_joined,
                        "last_login": user.last_login,
                    }
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "status": "error",
                "message": "Login failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    """
    Handle user logout.
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete auth token
            request.user.auth_token.delete()

            # Logout user (clears session)
            logout(request)

            return Response(
                {
                    "status": "success",
                    "message": "Logged out successfully.",
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": "Logout failed.",
                    "errors": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    """
    Handle viewing and updating user profile.
    GET  /api/auth/profile/
    PATCH /api/auth/profile/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get current user profile.
        """
        serializer = UserProfileSerializer(request.user)
        return Response(
            {
                "status": "success",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request):
        """
        Update current user profile.
        Partial updates allowed.
        """
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True  # Allow partial updates
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Profile updated successfully.",
                    "user": serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "status": "error",
                "message": "Profile update failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )