from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    Includes read-only fields 'username' and 'profile_image' sourced from the sender.
    """
    username = serializers.ReadOnlyField(source='sender.username')
    profile_image = serializers.ReadOnlyField(source='sender.profile.image.url')

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'recipient', 'notification_type', 'username', 'post', 'created_at', 'profile_image']
