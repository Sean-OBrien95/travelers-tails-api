from rest_framework import serializers
from profiles.serializers import ProfileSerializer
from .models import ChatMessage


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for chat messages with sender and receiver profiles.
    """
    receiver_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'sender_profile', 'receiver_profile', 'message', 'date_sent']
    
    def __init__(self, *args, **kwargs):
        super(CustomMessageSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2