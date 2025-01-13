
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer
from rest_framework import status, generics, permissions


class RegisterView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = CustomUser.objects.filter(username=username).first()
        if user and user.check_password(password):
            'token', Token.objects.get_or_create(user=user)
            return Response({'token': 'token'.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()  # Fetch all user objects
    serializer_class = CustomUserSerializer  # Use the UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to access this endpoint (e.g., signup)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()  # Fetch all user objects
    serializer_class = CustomUserSerializer  # Use the UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    

class FollowUserView(generics.GenericAPIView):
    
    permission_classes = ["permissions.IsAuthenticated"]

    def post(self, request, *args, **kwargs):
        user_to_follow_id = kwargs.get("user_id")
        try:
            user_to_follow = CustomUser.objects.all()
            if user_to_follow == request.user:
                return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.following.add(user_to_follow)
            return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(generics.GenericAPIView):
    
    permission_classes = ["permissions.IsAuthenticated"]

    def post(self, request, *args, **kwargs):
        user_to_unfollow_id = kwargs.get("user_id")
        try:
            user_to_unfollow = CustomUser.objects.all()
            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
