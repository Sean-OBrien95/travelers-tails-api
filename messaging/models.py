from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile


class ChatMessage(models.Model):
    """
    Model for sending and receiving messages from users.
    """
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="received_messages")
    message = models.CharField(max_length=5000)
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_sent']
        verbose_name = "message"

    def __str__(self):
        return f"From: {self.sender.username} - To: {self.receiver.username}"

    def get_sender_profile(self):
        """
        Retrieve the sender's profile.
        """
        return Profile.objects.get(user=self.sender)

    def get_receiver_profile(self):
        """
        Retrieve the receiver's profile.
        """
        return Profile.objects.get(user=self.receiver)