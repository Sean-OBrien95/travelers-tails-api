from django.test import TestCase
from django.contrib.auth.models import User
from followers.models import Follower
from django.db.utils import IntegrityError


class FollowerTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')
        self.user2 = User.objects.create_user(
            username='user2', password='password')
        self.user3 = User.objects.create_user(
            username='user3', password='password')

    def test_follower_creation(self):
        # Create a follower relationship
        follower = Follower.objects.create(
             owner=self.user1, followed=self.user2)

        # Check if the follower relationship is created
        self.assertTrue(Follower.objects.filter(
            owner=self.user1, followed=self.user2).exists())
        self.assertEqual(follower.owner, self.user1)
        self.assertEqual(follower.followed, self.user2)

    def test_follower_unique_constraint(self):
        # Create the first follower relationship
        Follower.objects.create(owner=self.user1, followed=self.user2)

        # Attempt to create a duplicate follower relationship
        with self.assertRaises(IntegrityError):
            Follower.objects.create(owner=self.user1, followed=self.user2)

    def test_follower_str_representation(self):
        follower = Follower.objects.create(
            owner=self.user1, followed=self.user2)
        self.assertEqual(str(follower), f'{self.user1} {self.user2}')

    def test_follower_ordering(self):
        follower1 = Follower.objects.create(
            owner=self.user1, followed=self.user2)
        follower2 = Follower.objects.create(
            owner=self.user2, followed=self.user3)

        # Assuming follower2 was created after follower1
        followers = list(Follower.objects.all())
        self.assertEqual(followers[0], follower2)
        self.assertEqual(followers[1], follower1)
