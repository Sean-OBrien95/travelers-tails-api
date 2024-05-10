from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from posts.models import Post
from likes.models import Like
from followers.models import Follower
from comments.models import Comment
from rest_framework import serializers

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient}"


def create_notification_on_like(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.owner,
            sender=instance.owner,
            notification_type='like',
            post=instance.post
        )

post_save.connect(create_notification_on_like, sender=Like)

def create_notification_on_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.followed_user,
            sender=instance.follower,
            notification_type='follow',
        )

post_save.connect(create_notification_on_follow, sender=Follower)

def create_notification_on_comment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.owner,
            sender=instance.owner,
            notification_type='comment',
            post=instance.post
        )

post_save.connect(create_notification_on_comment, sender=Comment)
