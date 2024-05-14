from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source='sender.username')
    profile_image = serializers.ReadOnlyField(source='sender.profile.image.url')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'content', 'timestamp', 'username', 'profile_image']

    def get_sender_name(self, obj):
        return obj.sender.username

class ConversationSerializer(serializers.ModelSerializer):

    sender_name = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source='sender.username')
    profile_image = serializers.ReadOnlyField(source='sender.profile.image.url')

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'sender_name', 'username', 'profile_image']