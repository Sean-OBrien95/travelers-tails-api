from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
from travelers_tails_api.permissions import IsOwnerOrReadOnly

class NotificationList(generics.ListCreateAPIView):
    """
    List all notifications and create a new notification.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve and delete a specific notification.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer