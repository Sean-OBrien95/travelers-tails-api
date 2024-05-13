from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source='sender.username')
    profile_id = serializers.ReadOnlyField(source='sender.profile.id')
    profile_image = serializers.ReadOnlyField(source='sender.profile.image.url')

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'recipient', 'notification_type', 'username', 'post', 'created_at']
