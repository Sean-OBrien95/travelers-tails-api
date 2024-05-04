from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Notification(models.Model):
    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )
    
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)