from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

# Create your views here.

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        unread_count = notifications.filter(is_read=False).count()

        data = {
            "notifications": [
                {
                    "id": n.id,
                    "actor": n.actor.username,
                    "verb": n.verb,
                    "target": str(n.target),
                    "timestamp": n.timestamp,
                    "is_read": n.is_read,
                }
                for n in notifications
            ],
            "unread_count": unread_count,
        }
        return Response(data, status=200)
