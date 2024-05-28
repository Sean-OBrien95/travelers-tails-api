from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post
from likes.models import Like
from comments.models import Comment
from notifications.models import Notification


class NotificationTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')
        self.user2 = User.objects.create_user(
            username='user2', password='password')
        self.post = Post.objects.create(
            owner=self.user1, content='Test Post')

    def test_create_like_notification(self):
        # Create a Like instance to trigger the signal
        like = Like.objects.create(owner=self.user2, post=self.post)

        # Check that the notification was created
        notification = Notification.objects.get(
            recipient=self.user1, sender=self.user2, notification_type='like')
        self.assertIsNotNone(notification)
        self.assertEqual(notification.post, self.post)
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.notification_type, 'like')

    def test_create_comment_notification(self):
        # Create a Comment instance to trigger the signal
        comment = Comment.objects.create(
            owner=self.user2, post=self.post, content='Nice post!')

        # Check that the notification was created
        notification = Notification.objects.get(
             recipient=self.user1,
             sender=self.user2,
             notification_type='comment')
        self.assertIsNotNone(notification)
        self.assertEqual(notification.post, self.post)
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.notification_type, 'comment')

    def test_single_notification_on_like(self):
        # Create a Like instance to trigger the signal
        like = Like.objects.create(owner=self.user2, post=self.post)

        # Ensure only one notification is created
        notifications = Notification.objects.filter(
             recipient=self.user1, sender=self.user2, notification_type='like')
        self.assertEqual(notifications.count(), 1)

    def test_create_multiple_comment_notifications(self):
        # Create two Comment instances to trigger the signal twice
        comment1 = Comment.objects.create(
             owner=self.user2, post=self.post, content='Nice post!')
        comment2 = Comment.objects.create(
             owner=self.user2, post=self.post, content='Another comment!')

        # Check that two notifications were created
        notifications = Notification.objects.filter(
            recipient=self.user1,
            sender=self.user2,
            notification_type='comment')
        self.assertEqual(notifications.count(), 2)
