from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.conf import settings

# Models

class CustomUser(AbstractUser):
        
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True,)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True,)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following_set', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers_set', blank=True)
    
    def __str__(self):
        return self.username


class Post(models.Model):
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts_posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    
    post = models.ForeignKey('user_account.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate relationships

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"