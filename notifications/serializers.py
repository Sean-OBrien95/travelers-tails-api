from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'recipient', 'notification_type', 'username', 'post', 'created_at']
