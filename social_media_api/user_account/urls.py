from django.urls import path
from .views import RegisterView, LoginView, FollowUserView, UnfollowUserView, UserListView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.http import JsonResponse


# Root endpoint for the user account API
def user_account_root(request):
    return JsonResponse({
        "message": "Welcome to my BE Capstone: SOCIAL MEDIA API Project",
        "endpoints": [
            "register/",
            "login/",
            "token/refresh/",
            "token/verify/",
            "follow/<user_id>/",
            "unfollow/<user_id>/",
            "users/",
            "users/<id>/"
        ]
    })


urlpatterns = [
    # Directly serve the user account root
    path('', user_account_root, name='user_account_root'),  # This is now the root endpoint

    # User registration and authentication routes
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Follow and unfollow user routes
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),

    # User listing and detail routes
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]