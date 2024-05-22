from rest_framework import generics
from django.db.models import Q, Subquery, OuterRef
from django.contrib.auth.models import User
from .models import ChatMessage
from .serializers import MessageSerializer
from .profiles.serializers import ProfileSerializer


class CustomInbox(generics.ListAPIView):
    """
    Custom view for inbox messages.
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        messages = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__receiver=user_id) | Q(receiver__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), receiver=user_id) |
                            Q(receiver=OuterRef('id'), sender=user_id)
                        ).order_by('-id')[:1].values_list('id', flat=True)
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")
        return messages

class CustomGetMessages(generics.ListAPIView):
    """
    View for retrieving messages between different users.
    """
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']
        messages = ChatMessage.objects.filter(sender__in=[sender_id, receiver_id], receiver__in=[sender_id, receiver_id])
        return messages

class CustomSendMessages(generics.CreateAPIView):
    """
    View for sending messages.
    """
    serializer_class = MessageSerializer

class UserSearchView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        users = User.objects.filter(username__icontains=username)
        return users
