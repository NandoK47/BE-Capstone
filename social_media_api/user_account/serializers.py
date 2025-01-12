from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import CustomUser, User


User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    bio = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password','bio', 'profile_picture', 'followers']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        token, created = Token.objects.create(user=user)
        user.save()
        return user
    
    

class FollowSerializer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many=True)
    following = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'following', 'followers']
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # This should be the user model you're using
        fields = ['username', 'email', 'password']  # Adjust fields as needed

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user